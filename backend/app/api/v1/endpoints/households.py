import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.api import deps
from app.models.user import User, UserRole
from app.models.geography import Village, Uzlah, District
from app.models.household import (
    Household,
    HouseholdMember,
    IdType,
    IdVerificationStatus,
    HousingType,
    HouseholdStatus,
)
from app.schemas.household import HouseholdOut, HouseholdCreate, HouseholdListItem
from app.services.duplicate_service import DuplicateDetectionEngine

router = APIRouter()


@router.get("", response_model=List[HouseholdListItem])
def list_households(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    search: Optional[str] = Query(None, description="بحث بالاسم، رقم الملف، أو رقم الهوية"),
    id_type: Optional[IdType] = Query(None, description="تصفية حسب نوع الهوية (وطنية / مؤقتة)"),
    housing_type: Optional[HousingType] = Query(None, description="تصفية حسب نوع السكن"),
    district_id: Optional[str] = Query(None, description="تصفية حسب المديرية"),
) -> List[HouseholdListItem]:
    """
    استعراض وتصفية ملفات الأسر مع مراعاة تجهيل الهويات لمحلل البيانات
    List Households with Search, Filters, and Analyst Pseudonymization
    """
    query = db.query(Household).filter(Household.status == HouseholdStatus.ACTIVE)

    # تطبيق البحث
    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Household.head_full_name.ilike(search_term),
                Household.file_number.ilike(search_term),
                Household.id_number.ilike(search_term),
                Household.phone_number.ilike(search_term),
            )
        )

    if id_type:
        query = query.filter(Household.id_type == id_type)

    if housing_type:
        query = query.filter(Household.housing_type == housing_type)

    # التقييد بالنطاق الجغرافي للباحثين الميدانيين
    if current_user.role == UserRole.FIELD_RESEARCHER:
        user_districts = deps.get_user_scopes(current_user)
        if user_districts:
            query = query.join(Village).join(Uzlah).filter(Uzlah.district_id.in_(user_districts))

    if district_id:
        query = query.join(Village).join(Uzlah).filter(Uzlah.district_id == district_id)

    total_results = query.order_by(desc(Household.created_at)).offset(skip).limit(limit).all()

    # تجهيل البيانات إذا كان المستخدم محلل بيانات (Data Anonymization Policy)
    is_analyst = (current_user.role == UserRole.DATA_ANALYST)

    items = []
    for h in total_results:
        item = HouseholdListItem(
            id=h.id,
            file_number=h.file_number,
            pseudo_id=h.pseudo_id,
            head_full_name="[مستفيد مجهل الهوية]" if is_analyst else h.head_full_name,
            id_type=h.id_type,
            id_number="[محجوب للتحليل]" if is_analyst else h.id_number,
            id_verification_status=h.id_verification_status,
            phone_number=None if is_analyst else h.phone_number,
            housing_type=h.housing_type,
            monthly_income=float(h.monthly_income),
            status=h.status,
            members_count=len(h.members),
            created_at=h.created_at,
        )
        items.append(item)

    return items


@router.get("/{household_id}", response_model=HouseholdOut)
def get_household(
    household_id: uuid.UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Household:
    """استرجاع الملف التفصيلي للأسرة وأفرادها"""
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ملف الأسرة غير موجود",
        )

    # منع محلل البيانات من استعراض التفاصيل الصريحة للأفراد
    if current_user.role == UserRole.DATA_ANALYST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="غير مصرح لمحلل البيانات باستعراض الملفات الفردية الصريحة للأسر",
        )

    return household


@router.post("", response_model=HouseholdOut, status_code=status.HTTP_201_CREATED)
def create_household(
    household_in: HouseholdCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.require_role([
        UserRole.SYSTEM_ADMIN,
        UserRole.BENEFICIARY_OFFICER,
        UserRole.FIELD_RESEARCHER,
    ])),
) -> Household:
    """
    تسجيل أسرة جديدة مع التحقق الصارم ودعم المعرفات المؤقتة
    Create New Household with Validation & Auto Duplicate Check
    """
    # 1. التحقق من القرية والموقع
    village = db.query(Village).filter(Village.id == household_in.village_id).first()
    if not village:
        raise HTTPException(status_code=400, detail="القرية أو الحي المحدد غير موجود بالنظام")

    # 2. معالجة حالات عدم توفر الوثائق الرسمية (Temporary ID Flow)
    if household_in.id_type == IdType.TEMPORARY_ID:
        if not household_in.attestation_source or len(household_in.attestation_source.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="حقل مصدر الإفادة المحلية (عاقل الحارة / اللجنة المجتمعية) إلزامي عند اختيار معرف مؤقت",
            )
        verification_status = IdVerificationStatus.LOCAL_ATTESTATION
        # توليد رقم المعرف المؤقت تلقائياً إن لم يُمرر
        if not household_in.id_number:
            uzlah = db.query(Uzlah).filter_by(id=village.uzlah_id).first()
            dist = db.query(District).filter_by(id=uzlah.district_id).first()
            id_num = f"TMP-{dist.governorate_id}-2026-{uuid.uuid4().hex[:6].upper()}"
        else:
            id_num = household_in.id_number
    else:
        if not household_in.id_number:
            raise HTTPException(status_code=422, detail="رقم الوثيقة الرسمية إلزامي")
        id_num = household_in.id_number
        verification_status = IdVerificationStatus.VERIFIED_OFFICIAL

    # 3. التحقق من عدم تكرار الرقم الوطني المباشر
    if household_in.id_type == IdType.NATIONAL_ID:
        existing = db.query(Household).filter(
            Household.id_number == id_num,
            Household.status == HouseholdStatus.ACTIVE,
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"الرقم الوطني ({id_num}) مسجل مسبقاً برقم الملف {existing.file_number}",
            )

    # 4. توليد أرقام الملف والمعرف التحليلي المستعار
    seq = db.query(Household).count() + 1
    file_num = f"RSH-2026-{seq:05d}"
    pseudo = f"ANON-YE-{uuid.uuid4().hex[:6].upper()}"

    household = Household(
        file_number=file_num,
        pseudo_id=pseudo,
        head_full_name=household_in.head_full_name,
        id_type=household_in.id_type,
        id_number=id_num,
        id_verification_status=verification_status,
        attestation_source=household_in.attestation_source,
        phone_number=household_in.phone_number,
        village_id=household_in.village_id,
        address_details=household_in.address_details,
        housing_type=household_in.housing_type,
        monthly_income=household_in.monthly_income,
        status=HouseholdStatus.ACTIVE,
        created_by_user_id=current_user.id,
    )
    db.add(household)
    db.flush()

    # 5. إضافة أفراد الأسرة
    for m in household_in.members:
        member = HouseholdMember(
            household_id=household.id,
            full_name=m.full_name,
            relationship=m.relationship,
            gender=m.gender,
            approximate_age=m.approximate_age,
            birth_date=m.birth_date,
            health_status=m.health_status,
            disability_type=m.disability_type,
            education_level=m.education_level,
            employment_status=m.employment_status,
        )
        db.add(member)

    db.commit()
    db.refresh(household)

    # 6. تشغيل فحص التكرار التلقائي في الخلفية لإشعار النظام بأي اشتباه
    DuplicateDetectionEngine.scan_household_duplicates(db, household)

    return household
