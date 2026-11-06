import enum
import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import String, Integer, Numeric, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import BaseModel


class DocumentType(str, enum.Enum):
    NATIONAL_ID = "NATIONAL_ID"
    FAMILY_CARD = "FAMILY_CARD"
    MEDICAL_REPORT = "MEDICAL_REPORT"
    RENTAL_CONTRACT = "RENTAL_CONTRACT"
    COMMUNITY_ATTESTATION = "COMMUNITY_ATTESTATION"
    OTHER = "OTHER"


class OCRStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MANUALLY_VERIFIED = "MANUALLY_VERIFIED"


class Document(BaseModel):
    """جدول الوثائق المرفوعة في المستودع الآمن"""
    __tablename__ = "documents"

    household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True)
    doc_type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType, name="document_type_enum", native_enum=False),
        nullable=False,
    )
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    ocr_status: Mapped[OCRStatus] = mapped_column(
        Enum(OCRStatus, name="ocr_status_enum", native_enum=False),
        nullable=False,
        default=OCRStatus.PENDING,
    )
    uploaded_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)

    ocr_extraction: Mapped[Optional["OCRExtraction"]] = relationship("OCRExtraction", back_populates="document", uselist=False)


class OCRExtraction(BaseModel):
    """نتائج استخراج النصوص العربية مع نسب الثقة والتحقق البشري"""
    __tablename__ = "ocr_extractions"

    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), unique=True, nullable=False)
    extracted_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    raw_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    overall_confidence: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0.0)
    human_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verified_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    document: Mapped["Document"] = relationship("Document", back_populates="ocr_extraction")
