import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User, UserRole
from app.models.household import Household, HouseholdStatus
from app.models.duplicate import DuplicateSuspicion, ResolutionStatus
from app.schemas.duplicate import DuplicateSuspicionOut, DuplicateResolutionRequest

router = APIRouter()


@router.get("", response_model=List[DuplicateSuspicionOut])
def list_duplicate_suspicions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([
        UserRole.SYSTEM_ADMIN,
        UserRole.PROGRAMS_OFFICER,
        UserRole.AUDITOR,
        UserRole.MANAGER,
        UserRole.BENEFICIARY_OFFICER,
    ])),
) -> List[DuplicateSuspicion]:
    """استعراض قائمة حالات الاشتباه بالتكرار قيد المراجعة"""
    return db.query(DuplicateSuspicion).filter(
        DuplicateSuspicion.resolution_status == ResolutionStatus.PENDING
    ).order_by(DuplicateSuspicion.similarity_score.desc()).all()


@router.post("/{suspicion_id}/resolve", response_model=DuplicateSuspicionOut)
def resolve_duplicate_suspicion(
    suspicion_id: uuid.UUID,
    resolve_data: DuplicateResolutionRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([
        UserRole.PROGRAMS_OFFICER,
        UserRole.AUDITOR,
        UserRole.MANAGER,
    ])),
) -> DuplicateSuspicion:
    """
    معالجة حالة الاشتباه بالتكرار: اعتماد الدمج المنطقي أو إقرار خطأ الاشتباه (False Positive)
    Resolve Duplicate Suspicion with Human-in-the-Loop Audit Trail
    """
    suspicion = db.query(DuplicateSuspicion).filter_by(id=suspicion_id).first()
    if not suspicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="سجل الاشتباه بالتكرار غير موجود",
        )

    if len(resolve_data.resolution_reason.strip()) < 15:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="يجب كتابة مبرر ومسوغ بشري واضح ومفصل (15 حرفاً على الأقل)",
        )

    suspicion.resolution_status = resolve_data.resolution_status
    suspicion.resolution_reason = resolve_data.resolution_reason

    # تطبيق مبدأ الاعتماد الثنائي
    if not suspicion.reviewed_by_user_id:
        suspicion.reviewed_by_user_id = current_user.id
    else:
        suspicion.audited_by_user_id = current_user.id

    # إذا تم تأكيد التطابق والدمج المنطقي
    if resolve_data.resolution_status == ResolutionStatus.CONFIRMED_MERGED:
        if not resolve_data.primary_household_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="يجب تحديد السجل الأساسي (Master Household) عند الدمج",
            )
        # تحويل السجل الثانوي إلى MERGED_DUPLICATE دون حذفه لحفظ السجل الرقابي
        secondary_id = (
            suspicion.matched_household_id
            if resolve_data.primary_household_id == suspicion.source_household_id
            else suspicion.source_household_id
        )
        secondary = db.query(Household).filter_by(id=secondary_id).first()
        if secondary:
            secondary.status = HouseholdStatus.MERGED_DUPLICATE

    db.commit()
    db.refresh(suspicion)
    return suspicion
