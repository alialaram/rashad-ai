from app.core.database import SessionLocal
from app.models.household import Household, IdType
from app.models.geography import Village
from app.models.duplicate import DuplicateSuspicion


def test_auth_login_success(client):
    """اختبار تسجيل الدخول الناجح وإصدار رمز JWT"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@2026"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "SYSTEM_ADMIN"
    assert data["username"] == "admin"


def test_auth_login_invalid_password(client):
    """اختبار رفض تسجيل الدخول بكلمة مرور خاطئة"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "WrongPassword"},
    )
    assert response.status_code == 401
    assert "غير صحيحة" in response.json()["detail"]


def test_auth_me_protected(client):
    """اختبار الوصول لمسار الحساب المحمي"""
    # 1. بدون توكن -> 401
    res_unauth = client.get("/api/v1/auth/me")
    assert res_unauth.status_code == 401

    # 2. بتوكن صالح -> 200
    login_res = client.post("/api/v1/auth/login", json={"username": "researcher_sanaa", "password": "Sanaa@2026"})
    token = login_res.json()["access_token"]
    res_auth = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_auth.status_code == 200
    assert res_auth.json()["username"] == "researcher_sanaa"
    assert res_auth.json()["role"] == "FIELD_RESEARCHER"


def test_list_households_with_roles(client):
    """اختبار استعراض الأسر وتطبيق سياسة تجهيل البيانات لمحلل البيانات"""
    # تسجيل دخول الباحث
    res_token = client.post("/api/v1/auth/login", json={"username": "beneficiary_officer", "password": "Register@2026"}).json()
    headers_officer = {"Authorization": f"Bearer {res_token['access_token']}"}

    res_officer = client.get("/api/v1/households?limit=5", headers=headers_officer)
    assert res_officer.status_code == 200
    data_officer = res_officer.json()
    assert len(data_officer) > 0
    # موظف التسجيل يرى الاسم الصريح
    assert data_officer[0]["head_full_name"] != "[مستفيد مجهل الهوية]"

    # تسجيل دخول محلل البيانات
    res_analyst_token = client.post("/api/v1/auth/login", json={"username": "analyst", "password": "Analyst@2026"}).json()
    headers_analyst = {"Authorization": f"Bearer {res_analyst_token['access_token']}"}

    res_analyst = client.get("/api/v1/households?limit=5", headers=headers_analyst)
    assert res_analyst.status_code == 200
    data_analyst = res_analyst.json()
    # محلل البيانات يخضع للتجهيل الإحصائي التام
    assert data_analyst[0]["head_full_name"] == "[مستفيد مجهل الهوية]"
    assert data_analyst[0]["id_number"] == "[محجوب للتحليل]"
    assert data_analyst[0]["phone_number"] is None


def test_create_household_with_temporary_id(client):
    """اختبار إنشاء أسرة بمعرف مؤقت والتحقق من إلزامية مصدر الإفادة"""
    session = SessionLocal()
    village = session.query(Village).first()
    session.close()

    res_token = client.post("/api/v1/auth/login", json={"username": "beneficiary_officer", "password": "Register@2026"}).json()
    headers = {"Authorization": f"Bearer {res_token['access_token']}"}

    # 1. محاولة إنشاء معرف مؤقت دون مصدر إفادة -> يجب أن يفشل 422
    payload_fail = {
        "head_full_name": "سالم علي محمد العديني",
        "id_type": "TEMPORARY_ID",
        "attestation_source": None,
        "village_id": str(village.id),
        "housing_type": "DISPLACED_CAMP",
        "monthly_income": 0,
        "members": [],
    }
    res_fail = client.post("/api/v1/households", json=payload_fail, headers=headers)
    assert res_fail.status_code == 422
    assert "مصدر الإفادة المحلية" in res_fail.json()["detail"]

    # 2. إنشاء ناجح مع توثيق عاقل الحارة وتوليد المعرف المؤقت تلقائياً
    payload_success = {
        "head_full_name": "سالم علي محمد العديني",
        "id_type": "TEMPORARY_ID",
        "attestation_source": "عاقل مخيم النزوح: الشيخ عبدالقادر الصلوي - تلفون: 770998877",
        "phone_number": "770998877",
        "village_id": str(village.id),
        "housing_type": "DISPLACED_CAMP",
        "monthly_income": 0,
        "members": [
            {
                "full_name": "سالم علي محمد العديني",
                "relationship": "HEAD",
                "gender": "MALE",
                "approximate_age": 45,
                "health_status": "CHRONIC_DISEASE",
            }
        ],
    }
    res_success = client.post("/api/v1/households", json=payload_success, headers=headers)
    assert res_success.status_code == 201
    created_data = res_success.json()
    assert created_data["id_type"] == "TEMPORARY_ID"
    assert "TMP-" in created_data["id_number"]
    assert created_data["id_verification_status"] == "LOCAL_ATTESTATION"


def test_needs_assessment_endpoint(client):
    """اختبار نقطة نهاية استعراض مؤشر الاحتياج والبطاقة التفسيرية"""
    session = SessionLocal()
    household = session.query(Household).first()
    session.close()

    res_token = client.post("/api/v1/auth/login", json={"username": "programs_officer", "password": "Officer@2026"}).json()
    headers = {"Authorization": f"Bearer {res_token['access_token']}"}

    res = client.get(f"/api/v1/needs/{household.id}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["household_id"] == str(household.id)
    assert 0 <= data["calculated_score"] <= 100
    assert "factors_breakdown" in data
    assert "income_vulnerability" in data["factors_breakdown"]
    assert data["disclaimer_acknowledged"] is True
    assert "مؤشر إحصائي تجريبي استرشادي" in data["disclaimer_text_ar"]


def test_duplicates_list_and_resolution(client):
    """اختبار استعراض ومعالجة السجلات المكررة مع اشتراط المسوغ البشري"""
    session = SessionLocal()
    suspicion = session.query(DuplicateSuspicion).filter_by(resolution_status="PENDING").first()
    session.close()

    res_token = client.post("/api/v1/auth/login", json={"username": "auditor", "password": "Auditor@2026"}).json()
    headers = {"Authorization": f"Bearer {res_token['access_token']}"}

    # 1. قائمة الاشتباهات
    res_list = client.get("/api/v1/duplicates", headers=headers)
    assert res_list.status_code == 200
    assert len(res_list.json()) > 0

    if suspicion:
        # 2. محاولة معالجة بدون مسوغ كافٍ -> 422
        res_fail = client.post(
            f"/api/v1/duplicates/{suspicion.id}/resolve",
            json={"resolution_status": "FALSE_POSITIVE", "resolution_reason": "قصير"},
            headers=headers,
        )
        assert res_fail.status_code == 422

        # 3. معالجة ناجحة بمسوغ بشري مفصل
        res_success = client.post(
            f"/api/v1/duplicates/{suspicion.id}/resolve",
            json={
                "resolution_status": "FALSE_POSITIVE",
                "resolution_reason": "تم النزول الميداني والتحقق من أن الحالتين مختلفتان تماماً بالوثائق والمسكن والأسماء.",
            },
            headers=headers,
        )
        assert res_success.status_code == 200
        assert res_success.json()["resolution_status"] == "FALSE_POSITIVE"
