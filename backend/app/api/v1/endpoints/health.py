from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: datetime
    message_ar: str


@router.get("", response_model=HealthResponse)
def check_health() -> HealthResponse:
    """
    فحص صحة النظام وحالة عمل الواجهة الخلفية
    System Health and Service Status Check
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc),
        message_ar="منظومة رشاد AI تعمل بنجاح وحالتها مستقرة",
    )
