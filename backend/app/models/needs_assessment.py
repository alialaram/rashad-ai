import enum
import uuid
from typing import Dict, Any, Optional
from sqlalchemy import String, Numeric, Boolean, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import BaseModel


class PriorityTier(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class NeedsAssessment(BaseModel):
    """مؤشرات الاحتياج الوصفية الاسترشادية والبطاقة التفسيرية"""
    __tablename__ = "needs_assessments"

    household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True)
    calculated_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    priority_tier: Mapped[PriorityTier] = mapped_column(
        Enum(PriorityTier, name="priority_tier_enum", native_enum=False),
        nullable=False,
    )
    model_version: Mapped[str] = mapped_column(String(50), nullable=False, default="RULE_ENGINE_V1.0")
    factors_breakdown: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    disclaimer_acknowledged: Mapped[bool] = mapped_column(Boolean, default=True)
    evaluator_override_tier: Mapped[Optional[PriorityTier]] = mapped_column(
        Enum(PriorityTier, name="override_tier_enum", native_enum=False),
        nullable=True,
    )
    evaluator_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evaluated_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
