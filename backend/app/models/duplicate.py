import enum
import uuid
from typing import Dict, Any, Optional
from sqlalchemy import String, Numeric, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import BaseModel


class MatchType(str, enum.Enum):
    EXACT_NATIONAL_ID = "EXACT_NATIONAL_ID"
    EXACT_PHONE = "EXACT_PHONE"
    FUZZY_NAME_GEO = "FUZZY_NAME_GEO"


class ResolutionStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED_MERGED = "CONFIRMED_MERGED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class DuplicateSuspicion(BaseModel):
    """سجل حالات الاشتباه بالازدواجية والتكرار"""
    __tablename__ = "duplicate_suspicions"

    source_household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True)
    matched_household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True)
    
    match_type: Mapped[MatchType] = mapped_column(
        Enum(MatchType, name="match_type_enum", native_enum=False),
        nullable=False,
    )
    similarity_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    match_details: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    
    resolution_status: Mapped[ResolutionStatus] = mapped_column(
        Enum(ResolutionStatus, name="resolution_status_enum", native_enum=False),
        nullable=False,
        default=ResolutionStatus.PENDING,
    )
    resolution_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # الاعتماد الثنائي (Two-Person Rule)
    reviewed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    audited_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
