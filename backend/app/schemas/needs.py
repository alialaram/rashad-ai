import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.needs_assessment import PriorityTier


class NeedsAssessmentOut(BaseModel):
    id: Optional[uuid.UUID] = None
    household_id: uuid.UUID
    calculated_score: float
    priority_tier: PriorityTier
    tier_label_ar: str
    model_version: str
    factors_breakdown: Dict[str, Any]
    disclaimer_text_ar: str
    disclaimer_acknowledged: bool
    evaluator_override_tier: Optional[PriorityTier] = None
    evaluator_notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
