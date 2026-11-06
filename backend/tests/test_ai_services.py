from app.core.database import SessionLocal
from app.models.household import Household, HouseholdStatus
from app.models.needs_assessment import NeedsAssessment, PriorityTier
from app.models.duplicate import DuplicateSuspicion, MatchType
from app.services.needs_service import NeedsAssessmentEngine
from app.services.duplicate_service import DuplicateDetectionEngine


def test_needs_assessment_calculation():
    """اختبار محرك تقييم الاحتياج الوصفي والبطاقة التفسيرية"""
    session = SessionLocal()
    try:
        household = session.query(Household).filter_by(status=HouseholdStatus.ACTIVE).first()
        assert household is not None, "Need at least one household in DB"

        # 1. احتساب التقييم
        result = NeedsAssessmentEngine.evaluate_household(household, household.members)

        assert 0.0 <= result["calculated_score"] <= 100.0
        assert result["priority_tier"] in [PriorityTier.CRITICAL, PriorityTier.HIGH, PriorityTier.MEDIUM, PriorityTier.LOW]
        assert "income_vulnerability" in result["factors_breakdown"]
        assert "dependency_vulnerability" in result["factors_breakdown"]
        assert "health_vulnerability" in result["factors_breakdown"]
        assert "housing_vulnerability" in result["factors_breakdown"]
        assert result["disclaimer_acknowledged"] is True
        assert "مؤشر إحصائي تجريبي استرشادي" in result["disclaimer_text_ar"]

        # 2. تخزين التقييم
        assessment = NeedsAssessmentEngine.evaluate_and_store(session, household.id)
        assert assessment.id is not None
        assert assessment.household_id == household.id
        assert assessment.calculated_score == result["calculated_score"]

    finally:
        session.close()


def test_duplicate_detection_engine():
    """اختبار كشف التكرار الآلي ورصد الحالات المحقونة في البيانات الاصطناعية"""
    session = SessionLocal()
    try:
        # فحص شامل لقاعدة البيانات
        stats = DuplicateDetectionEngine.scan_all_database(session)

        # التحقق من رصد حالات الاشتباه المحقونة في البيانات الاصطناعية
        assert stats["total_suspicions"] > 0, "Expected duplicate suspicions to be found"
        assert stats["exact_id_matches"] >= 1, "Expected at least 1 exact ID match (injected case)"
        assert stats["exact_phone_matches"] >= 1, "Expected at least 1 exact phone match (injected case)"

        # التحقق من تسجيل الحالات في جدول duplicate_suspicions
        suspicions = session.query(DuplicateSuspicion).filter_by(resolution_status="PENDING").all()
        assert len(suspicions) == stats["total_suspicions"]
        
        # التأكد من عدم الدمج الآلي وبقاء الحالة PENDING للمراجعة البشرية
        for susp in suspicions:
            assert susp.resolution_status.value == "PENDING"
            assert susp.similarity_score > 0

    finally:
        session.close()


def test_arabic_name_normalization_and_fuzzy():
    """اختبار توحيد الحروف العربية ودقة المطابقة الاحتمالية"""
    name1 = "أحمد محمد على الصنعانى"
    name2 = "احمد محمد علي الصنعاني"
    sim = DuplicateDetectionEngine.calculate_name_similarity(name1, name2)
    assert sim == 100.0, f"Expected 100% similarity after normalization, got {sim}%"

    name3 = "محمد عبدالله صالح الهمداني"
    name4 = "محمد عبدالله صالح الحيدري"
    sim_partial = DuplicateDetectionEngine.calculate_name_similarity(name3, name4)
    assert 70.0 <= sim_partial <= 95.0, f"Expected partial similarity, got {sim_partial}%"
