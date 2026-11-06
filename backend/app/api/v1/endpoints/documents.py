import os
import uuid
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm.attributes import flag_modified

from app.api import deps
from app.core.config import settings
from app.models.user import User, UserRole
from app.models.household import Household
from app.models.document import Document, OCRExtraction, DocumentType, OCRStatus
from app.schemas.document import DocumentOut, DocumentVerificationRequest
from app.services.ocr_service import ArabicDocumentOCREngine

router = APIRouter()


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    household_id: uuid.UUID = Form(...),
    doc_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([
        UserRole.SYSTEM_ADMIN,
        UserRole.BENEFICIARY_OFFICER,
        UserRole.FIELD_RESEARCHER,
    ])),
) -> Document:
    """
    رفع وثيقة إثبات وتشغيل محرك OCR العربي لاستخراج الحقول
    Upload Document & Run Experimental Arabic OCR
    """
    household = db.query(Household).filter_by(id=household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="ملف الأسرة غير موجود")

    # فحص صيغة الملف
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"صيغة الملف غير مدعومة ({file.content_type}). الصيغ المدعومة: JPEG, PNG, PDF",
        )

    # حفظ الملف في المستودع المحلي الآمن
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1] or ".jpg"
    storage_filename = f"{household.id}_{uuid.uuid4().hex[:8]}{file_ext}"
    storage_path = os.path.join(settings.UPLOAD_DIR, storage_filename)

    file_bytes = await file.read()
    with open(storage_path, "wb") as f:
        f.write(file_bytes)

    # إنشاء سجل الوثيقة في قاعدة البيانات
    document = Document(
        household_id=household.id,
        doc_type=doc_type,
        storage_path=storage_path,
        mime_type=file.content_type,
        file_size_bytes=len(file_bytes),
        ocr_status=OCRStatus.PENDING,
        uploaded_by_user_id=current_user.id,
    )
    db.add(document)
    db.flush()

    # تشغيل استخراج الـ OCR التجريبي
    try:
        extracted_data, overall_conf, raw_text = ArabicDocumentOCREngine.process_document(storage_path)
        extraction = OCRExtraction(
            document_id=document.id,
            extracted_data=extracted_data,
            raw_text=raw_text,
            overall_confidence=overall_conf,
            human_verified=False,
        )
        db.add(extraction)
        document.ocr_status = OCRStatus.COMPLETED
    except Exception as e:
        document.ocr_status = OCRStatus.FAILED

    db.commit()
    db.refresh(document)
    return document


@router.post("/generate-demo/{household_id}", response_model=DocumentOut)
def generate_demo_document(
    household_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Document:
    """توليد وثيقة اصطناعية لأسرة بغرض الاختبار والمعاينة البصرية"""
    household = db.query(Household).filter_by(id=household_id).first()
    if not household:
        raise HTTPException(status_code=404, detail="ملف الأسرة غير موجود")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"DEMO_ID_{household.file_number}.jpg"
    storage_path = os.path.join(settings.UPLOAD_DIR, filename)

    ArabicDocumentOCREngine.generate_synthetic_id_card(
        output_path=storage_path,
        full_name=household.head_full_name,
        national_id=household.id_number,
        birth_date="1984-07-15",
    )

    document = Document(
        household_id=household.id,
        doc_type=DocumentType.NATIONAL_ID,
        storage_path=storage_path,
        mime_type="image/jpeg",
        file_size_bytes=os.path.getsize(storage_path),
        ocr_status=OCRStatus.COMPLETED,
        uploaded_by_user_id=current_user.id,
    )
    db.add(document)
    db.flush()

    # محاكاة نص الوثيقة
    simulated_text = (
        f"الجمهورية اليمنية\n"
        f"مصلحة الأحوال المدنية والسجل المدني\n"
        f"الاسم: {household.head_full_name}\n"
        f"الرقم الوطني: {household.id_number}\n"
        f"تاريخ الميلاد: 1984-07-15\n"
        f"محل الإصدار: صنعاء\n"
    )
    extracted_data, overall_conf, raw_text = ArabicDocumentOCREngine.process_document(storage_path, simulated_text=simulated_text)

    extraction = OCRExtraction(
        document_id=document.id,
        extracted_data=extracted_data,
        raw_text=raw_text,
        overall_confidence=overall_conf,
        human_verified=False,
    )
    db.add(extraction)
    db.commit()
    db.refresh(document)
    return document


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Document:
    """استرجاع تفاصيل الوثيقة ونتائج الـ OCR المرتبطة بها"""
    document = db.query(Document).filter_by(id=document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="الوثيقة غير موجودة")
    return document


@router.get("/{document_id}/file")
def get_document_file(
    document_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """استعراض أو تحميل ملف الوثيقة المحمي"""
    document = db.query(Document).filter_by(id=document_id).first()
    if not document or not os.path.exists(document.storage_path):
        raise HTTPException(status_code=404, detail="ملف الوثيقة غير موجود على الخادم")
    return FileResponse(document.storage_path, media_type=document.mime_type)


@router.post("/{document_id}/verify", response_model=DocumentOut)
def verify_document_extraction(
    document_id: uuid.UUID,
    verification: DocumentVerificationRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([
        UserRole.SYSTEM_ADMIN,
        UserRole.BENEFICIARY_OFFICER,
        UserRole.AUDITOR,
        UserRole.PROGRAMS_OFFICER,
    ])),
) -> Document:
    """
    اعتماد التحقق البشري من الحقول المستخرجة وتصحيح أي أخطاء قراءة آلياً
    Human-in-the-Loop Document Verification & Approval
    """
    document = db.query(Document).filter_by(id=document_id).first()
    if not document or not document.ocr_extraction:
        raise HTTPException(status_code=404, detail="سجل استخراج الوثيقة غير موجود")

    from sqlalchemy.orm import Session
    extraction = document.ocr_extraction
    
    # تحديث الحقول المستخرجة بالقيم المعتمدة بشرياً مع إشعار SQLAlchemy بالتعديل
    current_data = dict(extraction.extracted_data)
    for k, val in verification.verified_fields.items():
        if k in current_data:
            current_data[k]["value"] = val
            current_data[k]["human_corrected"] = True
            current_data[k]["requires_review"] = False
    
    extraction.extracted_data = current_data
    flag_modified(extraction, "extracted_data")

    extraction.human_verified = True
    extraction.verified_by_user_id = current_user.id
    extraction.verified_at = datetime.now(timezone.utc)
    document.ocr_status = OCRStatus.MANUALLY_VERIFIED

    db.commit()
    db.refresh(document)
    db.refresh(extraction)
    return document
