import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.duplicate import MatchType, ResolutionStatus


class DuplicateSuspicionOut(BaseModel):
    id: uuid.UUID
    source_household_id: uuid.UUID
    matched_household_id: uuid.UUID
    match_type: MatchType
    similarity_score: float
    match_details: Dict[str, Any]
    resolution_status: ResolutionStatus
    resolution_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DuplicateResolutionRequest(BaseModel):
    resolution_status: ResolutionStatus  # CONFIRMED_MERGED or FALSE_POSITIVE
    resolution_reason: str
    primary_household_id: Optional[uuid.UUID] = None  # السجل الأساسي في حال الدمج
