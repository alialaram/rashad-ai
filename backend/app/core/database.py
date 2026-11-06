from datetime import datetime, timezone
import uuid
from typing import Generator
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.config import settings

# PostgreSQL Engine via psycopg
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BaseModel(Base):
    """النموذج الأساسي لجميع جداول النظام مع معرف UUID وطوابع زمنية موحدة"""
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


def get_db() -> Generator[Session, None, None]:
    """Dependency لتوفير جلسة قاعدة البيانات وإغلاقها تلقائياً بعد انتهاء الطلب"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
