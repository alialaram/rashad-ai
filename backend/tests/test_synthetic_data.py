from app.core.database import SessionLocal
from app.models.household import Household, HouseholdMember, IdType, IdVerificationStatus
from app.models.geography import Governorate, District, Village


def test_synthetic_data_integrity():
    """التحقق من سلامة وجودة البيانات الاصطناعية وتنوعها"""
    session = SessionLocal()
    try:
        # 1. التحقق من وجود 150 أسرة اصطناعية
        households = session.query(Household).all()
        assert len(households) >= 150, "Expected at least 150 households"

        # 2. التحقق من وجود أسر بمعرفات مؤقتة ومصدر إفادة بديل
        undocumented = session.query(Household).filter(Household.id_type == IdType.TEMPORARY_ID).all()
        assert len(undocumented) > 0, "Expected at least some households with TEMPORARY_ID"
        for doc in undocumented:
            assert doc.attestation_source is not None, "Temporary ID must have an attestation source"
            assert doc.id_verification_status == IdVerificationStatus.LOCAL_ATTESTATION

        # 3. التحقق من ربط جميع الأسر بقرى ومديريات صحيحة
        for h in households[:20]:
            village = session.query(Village).filter_by(id=h.village_id).first()
            assert village is not None, f"Village not found for household {h.file_number}"

        # 4. التحقق من أفراد الأسرة
        total_members = session.query(HouseholdMember).count()
        assert total_members > len(households) * 2, "Expected average family size > 2"
        
        # 5. التحقق من وجود حالات أسرية خاصة (أمراض مزمنة أو إعاقات)
        vulnerable_members = session.query(HouseholdMember).filter(
            (HouseholdMember.health_status == "CHRONIC_DISEASE") | (HouseholdMember.disability_type.isnot(None))
        ).count()
        assert vulnerable_members > 0, "Expected vulnerable family members in synthetic dataset"

    finally:
        session.close()
