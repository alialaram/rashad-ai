from sqlalchemy import text
from app.core.database import engine, SessionLocal


def test_postgres_connection():
    """اختبار الاتصال المباشر بقاعدة بيانات PostgreSQL 18 المحلية"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1;"))
        assert result.scalar() == 1


def test_session_lifecycle():
    """اختبار دورة حياة جلسة قاعدة البيانات وإنشائها وإغلاقها"""
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT current_database();"))
        db_name = result.scalar()
        assert db_name == "rashad_ai_dev"
    finally:
        session.close()
