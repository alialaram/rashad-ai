import enum
import uuid
from typing import List, Optional
from datetime import date
from sqlalchemy import String, Numeric, Enum, Text, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship as sa_relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import BaseModel


class IdType(str, enum.Enum):
    NATIONAL_ID = "NATIONAL_ID"
    FAMILY_CARD = "FAMILY_CARD"
    TEMPORARY_ID = "TEMPORARY_ID"
    OTHER = "OTHER"


class IdVerificationStatus(str, enum.Enum):
    VERIFIED_OFFICIAL = "VERIFIED_OFFICIAL"
    LOCAL_ATTESTATION = "LOCAL_ATTESTATION"
    PENDING_REVIEW = "PENDING_REVIEW"


class HousingType(str, enum.Enum):
    OWNED = "OWNED"
    RENTED = "RENTED"
    DISPLACED_CAMP = "DISPLACED_CAMP"
    SHARED = "SHARED"
    MAKSHA = "MAKSHA"


class HouseholdStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    MERGED_DUPLICATE = "MERGED_DUPLICATE"


class RelationshipType(str, enum.Enum):
    HEAD = "HEAD"
    WIFE = "WIFE"
    SON = "SON"
    DAUGHTER = "DAUGHTER"
    PARENT = "PARENT"
    OTHER = "OTHER"


class HealthStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    CHRONIC_DISEASE = "CHRONIC_DISEASE"
    DISABILITY = "DISABILITY"


class EmploymentStatus(str, enum.Enum):
    EMPLOYED = "EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    UNABLE_TO_WORK = "UNABLE_TO_WORK"
    STUDENT = "STUDENT"


class Household(BaseModel):
    """ملف الأسرة الأساسي"""
    __tablename__ = "households"

    file_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    pseudo_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    # بيانات رب الأسرة
    head_full_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    id_type: Mapped[IdType] = mapped_column(
        Enum(IdType, name="id_type_enum", native_enum=False),
        nullable=False,
        default=IdType.NATIONAL_ID,
    )
    id_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    id_verification_status: Mapped[IdVerificationStatus] = mapped_column(
        Enum(IdVerificationStatus, name="id_verification_status_enum", native_enum=False),
        nullable=False,
        default=IdVerificationStatus.PENDING_REVIEW,
    )
    attestation_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(25), nullable=True, index=True)

    # الموقع والسكن
    village_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("villages.id"), nullable=False, index=True)
    address_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    housing_type: Mapped[HousingType] = mapped_column(
        Enum(HousingType, name="housing_type_enum", native_enum=False),
        nullable=False,
        default=HousingType.RENTED,
    )

    # الحالة المادية
    monthly_income: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    status: Mapped[HouseholdStatus] = mapped_column(
        Enum(HouseholdStatus, name="household_status_enum", native_enum=False),
        nullable=False,
        default=HouseholdStatus.ACTIVE,
    )

    # الرقابة وتتبع الإنشاء
    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)

    # العلاقات
    members: Mapped[List["HouseholdMember"]] = sa_relationship("HouseholdMember", back_populates="household", cascade="all, delete-orphan")


class HouseholdMember(BaseModel):
    """فرد من أفراد الأسرة"""
    __tablename__ = "household_members"

    household_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("households.id", ondelete="CASCADE"), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    relationship: Mapped[RelationshipType] = mapped_column(
        Enum(RelationshipType, name="relationship_type_enum", native_enum=False),
        nullable=False,
        default=RelationshipType.OTHER,
    )
    gender: Mapped[str] = mapped_column(String(10), nullable=False)  # MALE / FEMALE
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    approximate_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    health_status: Mapped[HealthStatus] = mapped_column(
        Enum(HealthStatus, name="health_status_enum", native_enum=False),
        nullable=False,
        default=HealthStatus.HEALTHY,
    )
    disability_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    education_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    employment_status: Mapped[EmploymentStatus] = mapped_column(
        Enum(EmploymentStatus, name="employment_status_enum", native_enum=False),
        nullable=False,
        default=EmploymentStatus.UNEMPLOYED,
    )

    household: Mapped["Household"] = sa_relationship("Household", back_populates="members")
