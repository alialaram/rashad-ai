import os
from app.core.database import SessionLocal
from app.models.household import Household
from app.services.ocr_service import ArabicDocumentOCREngine


def test_arabic_ocr_engine_text_extraction():
    """اختبار استخراج الحقول المهيكلة من نصوص الوثائق وحساب نسب الثقة"""
    sample_text = (
        "الجمهورية اليمنية\n"
        "وزارة الداخلية - مصلحة الأحوال المدنية\n"
        "بطاقة شخصية\n"
        "الاسم: محمد علي عبدالله الهمداني\n"
        "الرقم الوطني: 01998877665\n"
        "تاريخ الميلاد: 1988-11-20\n"
        "محل الإصدار: صنعاء\n"
    )
    fields = ArabicDocumentOCREngine.extract_id_fields(sample_text)

    # التحقق من دقة الاستخراج
    assert fields["national_id"]["value"] == "01998877665"
    assert fields["national_id"]["confidence"] >= 90.0
    assert fields["national_id"]["requires_review"] is False

    assert "محمد علي عبدالله الهمداني" in fields["full_name"]["value"]
    assert fields["full_name"]["confidence"] >= 90.0

    assert fields["birth_date"]["value"] == "1988-11-20"
    assert fields["issue_place"]["value"] == "صنعاء"


def test_generate_synthetic_id_card():
    """اختبار توليد بطاقة شخصية تجريبية كصورة صالحة"""
    test_img_path = "./storage/documents/test_id_card.jpg"
    ArabicDocumentOCREngine.generate_synthetic_id_card(
        output_path=test_img_path,
        full_name="علي يحيى حسين الصنعاني",
        national_id="01123456789",
        birth_date="1990-05-10",
    )
    assert os.path.exists(test_img_path)
    assert os.path.getsize(test_img_path) > 1000  # الصورة حقيقية وغير فارغة


def test_document_api_flow(client):
    """اختبار دورة حياة الوثيقة من التوليد والاستخراج إلى التحقق البشري"""
    session = SessionLocal()
    household = session.query(Household).first()
    session.close()

    res_token = client.post("/api/v1/auth/login", json={"username": "beneficiary_officer", "password": "Register@2026"}).json()
    headers = {"Authorization": f"Bearer {res_token['access_token']}"}

    # 1. توليد وثيقة تجريبية للأسرة
    res_gen = client.post(f"/api/v1/documents/generate-demo/{household.id}", headers=headers)
    assert res_gen.status_code == 200
    doc_data = res_gen.json()
    assert doc_data["doc_type"] == "NATIONAL_ID"
    assert doc_data["ocr_status"] == "COMPLETED"
    assert doc_data["ocr_extraction"] is not None
    assert doc_data["ocr_extraction"]["overall_confidence"] > 0
    assert doc_data["ocr_extraction"]["human_verified"] is False

    doc_id = doc_data["id"]

    # 2. اعتماد التحقق البشري وتصحيح حقل
    verified_payload = {
        "verified_fields": {
            "full_name": "علي يحيى حسين الصنعاني (معتمد يدوياً)",
            "national_id": doc_data["ocr_extraction"]["extracted_data"]["national_id"]["value"],
        },
        "reviewer_notes": "تمت المطابقة البصرية مع أصل البطاقة وإجازتها.",
    }
    res_verify = client.post(f"/api/v1/documents/{doc_id}/verify", json=verified_payload, headers=headers)
    assert res_verify.status_code == 200
    verified_data = res_verify.json()
    assert verified_data["ocr_status"] == "MANUALLY_VERIFIED"
    assert verified_data["ocr_extraction"]["human_verified"] is True
    assert "معتمد يدوياً" in verified_data["ocr_extraction"]["extracted_data"]["full_name"]["value"]
