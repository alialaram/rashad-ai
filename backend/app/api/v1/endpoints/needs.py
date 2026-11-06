import uuid
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.models.household import Household
from app.models.needs_assessment import NeedsAssessment
from app.schemas.needs import NeedsAssessmentOut
from app.services.needs_service import NeedsAssessmentEngine
from app.services.ml_service import ml_service

router = APIRouter()


@router.get("/metrics/ml-summary")
def get_ml_models_summary(
    current_user: User = Depends(deps.get_current_user),
) -> Dict[str, Any]:
    """
    استعراض حزمة نماذج تعلم الآلة ومقاييس الأداء والعناقيد الأسرية
    Get ML Models Performance Metrics and Vulnerability Clusters
    """
    return ml_service.get_system_metrics()


@router.get("/{household_id}", response_model=NeedsAssessmentOut)
def get_needs_assessment(
    household_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> NeedsAssessmentOut:
    """
    استعراض مؤشر الاحتياج الوصفي والبطاقة التفسيرية مع مقارنة تنبؤات تعلم الآلة
    Get Explainable Needs Assessment and Dual-Perspective ML Insights
    """
    household = db.query(Household).filter_by(id=household_id).first()
    if not household:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ملف الأسرة غير موجود",
        )

    # 1. احتساب التقييم الإرشادي الشفاف (Rule Baseline)
    eval_result = NeedsAssessmentEngine.evaluate_household(household, household.members)

    # 2. احتساب تنبؤات وعناقيد تعلم الآلة (Machine Learning Inference)
    ml_insights = ml_service.predict(household)

    # 3. حفظ التقييم إن لم يكن موجوداً
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
        ml_insights=ml_insights,
    )
