import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.models.household import Household
from app.models.needs_assessment import NeedsAssessment
from app.schemas.needs import NeedsAssessmentOut
from app.services.needs_service import NeedsAssessmentEngine

router = APIRouter()


@router.get("/{household_id}", response_model=NeedsAssessmentOut)
def get_needs_assessment(
    household_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> NeedsAssessmentOut:
    """
    استعراض مؤشر الاحتياج الوصفي والبطاقة التفسيرية لملف الأسرة
    Get Explainable Needs Assessment and Governance Breakdown
    """
    household = db.query(Household).filter_by(id=household_id).first()
    if not household:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ملف الأسرة غير موجود",
        )

    # احتساب التقييم الآني أو استرجاعه
    eval_result = NeedsAssessmentEngine.evaluate_household(household, household.members)

    # البحث عن تقييم سابق محفوظ
    assessment = db.query(NeedsAssessment).filter_by(household_id=household_id).first()
    if not assessment:
        assessment = NeedsAssessmentEngine.evaluate_and_store(db, household_id)

    return NeedsAssessmentOut(
        id=assessment.id,
        household_id=household.id,
        calculated_score=eval_result["calculated_score"],
        priority_tier=eval_result["priority_tier"],
        tier_label_ar=eval_result["tier_label_ar"],
        model_version=eval_result["model_version"],
        factors_breakdown=eval_result["factors_breakdown"],
        disclaimer_text_ar=eval_result["disclaimer_text_ar"],
        disclaimer_acknowledged=eval_result["disclaimer_acknowledged"],
        evaluator_override_tier=assessment.evaluator_override_tier,
        evaluator_notes=assessment.evaluator_notes,
        created_at=assessment.created_at,
    )
