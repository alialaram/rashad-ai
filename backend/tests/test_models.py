from sqlalchemy import inspect
from app.core.database import engine, Base
import app.models  # noqa: F401


def test_create_all_tables():
    """اختبار إنشاء كافة الجداول الكينونية في قاعدة بيانات PostgreSQL"""
    Base.metadata.create_all(bind=engine)
    
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    expected_tables = [
        "governorates",
        "districts",
        "uzlahs",
        "villages",
        "users",
        "user_scopes",
        "households",
        "household_members",
        "documents",
        "ocr_extractions",
        "needs_assessments",
        "duplicate_suspicions",
        "assistance_requests",
        "request_approvals",
        "audit_logs",
    ]
    
    for table in expected_tables:
        assert table in table_names, f"Table '{table}' was not created in database!"
