import enum
import uuid
from typing import Optional, List
from sqlalchemy import String, Numeric, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import BaseModel


class ProgramType(str, enum.Enum):
    POOR_AND_NEEDY = "POOR_AND_NEEDY"
    DEBTORS_GHARIMEEN = "DEBTORS_GHARIMEEN"
    MEDICAL_AID = "MEDICAL_AID"
    DISASTER_RELIEF = "DISASTER_RELIEF"
    MARRIAGE_AID = "MARRIAGE_AID"
    OTHER = "OTHER"


class RequestStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    FIELD_SURVEY = "FIELD_SURVEY"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"


class ApprovalDecision(str, enum.Enum):
    RECOMMENDED = "RECOMMENDED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RETURNED_FOR_INFO = "RETURNED_FOR_INFO"


class AssistanceRequest(BaseModel):
    """طلبات المساعدات"""
    __tablename__ = "assistance_requests"

    request_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True)
    program_type: Mapped[ProgramType] = mapped_column(
        Enum(ProgramType, name="program_type_enum", native_enum=False),
        nullable=False,
    )
    current_status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, name="request_status_enum", native_enum=False),
        nullable=False,
        default=RequestStatus.SUBMITTED,
    )
    requested_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    approved_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)

    approvals: Mapped[List["RequestApproval"]] = relationship("RequestApproval", back_populates="request", cascade="all, delete-orphan")


class RequestApproval(BaseModel):
    """سجل المراجعات والاعتمادات المتسلسلة أو اللجانية"""
    __tablename__ = "request_approvals"

    request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assistance_requests.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    approval_level: Mapped[str] = mapped_column(String(50), nullable=False)
    decision: Mapped[ApprovalDecision] = mapped_column(
        Enum(ApprovalDecision, name="approval_decision_enum", native_enum=False),
        nullable=False,
    )
    decision_notes: Mapped[str] = mapped_column(Text, nullable=False)

    request: Mapped["AssistanceRequest"] = relationship("AssistanceRequest", back_populates="approvals")
