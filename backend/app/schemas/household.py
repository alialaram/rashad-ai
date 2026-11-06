import uuid
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field

from app.models.household import (
    IdType,
    IdVerificationStatus,
    HousingType,
    HouseholdStatus,
    RelationshipType,
    HealthStatus,
    EmploymentStatus,
)


class HouseholdMemberBase(BaseModel):
    full_name: str
    relationship: RelationshipType
    gender: str
    approximate_age: Optional[int] = None
    birth_date: Optional[date] = None
    health_status: HealthStatus = HealthStatus.HEALTHY
    disability_type: Optional[str] = None
    education_level: Optional[str] = None
    employment_status: EmploymentStatus = EmploymentStatus.UNEMPLOYED


class HouseholdMemberCreate(HouseholdMemberBase):
    pass


class HouseholdMemberOut(HouseholdMemberBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class HouseholdCreate(BaseModel):
    head_full_name: str
    id_type: IdType = IdType.NATIONAL_ID
    id_number: Optional[str] = None  # إذا كان None ونوع الهوية TEMPORARY_ID يتم توليده آلياً
    attestation_source: Optional[str] = None  # إلزامي في حال المعرف المؤقت
    phone_number: Optional[str] = None
    village_id: uuid.UUID
    address_details: Optional[str] = None
    housing_type: HousingType = HousingType.RENTED
    monthly_income: float = Field(default=0.0, ge=0.0)
    members: List[HouseholdMemberCreate] = []


class HouseholdListItem(BaseModel):
    id: uuid.UUID
    file_number: str
    pseudo_id: str
    head_full_name: str
    id_type: IdType
    id_number: str
    id_verification_status: IdVerificationStatus
    phone_number: Optional[str] = None
    housing_type: HousingType
    monthly_income: float
    status: HouseholdStatus
    members_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class HouseholdOut(BaseModel):
    id: uuid.UUID
    file_number: str
    pseudo_id: str
    head_full_name: str
    id_type: IdType
    id_number: str
    id_verification_status: IdVerificationStatus
    attestation_source: Optional[str] = None
    phone_number: Optional[str] = None
    village_id: uuid.UUID
    address_details: Optional[str] = None
    housing_type: HousingType
    monthly_income: float
    status: HouseholdStatus
    members: List[HouseholdMemberOut] = []
    created_at: datetime

    class Config:
        from_attributes = True
