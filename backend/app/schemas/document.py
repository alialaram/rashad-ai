import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.document import DocumentType, OCRStatus


class OCRExtractionOut(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    extracted_data: Dict[str, Any]
    raw_text: Optional[str] = None
    overall_confidence: float
    human_verified: bool
    verified_by_user_id: Optional[uuid.UUID] = None
    verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: uuid.UUID
    household_id: uuid.UUID
    doc_type: DocumentType
    storage_path: str
    mime_type: str
    file_size_bytes: int
    ocr_status: OCRStatus
    created_at: datetime
    ocr_extraction: Optional[OCRExtractionOut] = None

    class Config:
        from_attributes = True


class DocumentVerificationRequest(BaseModel):
    verified_fields: Dict[str, Any]  # الحقول بعد المراجعة والتصحيح البشري
    reviewer_notes: Optional[str] = None
