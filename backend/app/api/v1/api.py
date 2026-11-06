from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, households, needs, duplicates, documents

api_router = APIRouter()

# نقاط النهاية المعتمدة للإصدار الأول
api_router.include_router(health.router, prefix="/health", tags=["الصحة والمراقبة - Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["المصادقة والأمان - Authentication"])
api_router.include_router(households.router, prefix="/households", tags=["إدارة الأسر والمستفيدين - Households"])
api_router.include_router(needs.router, prefix="/needs", tags=["تقييم الاحتياج ودعم القرار - Needs Assessment"])
api_router.include_router(duplicates.router, prefix="/duplicates", tags=["كشف التكرار والازدواجية - Duplicate Detection"])
api_router.include_router(documents.router, prefix="/documents", tags=["ذكاء الوثائق والـ OCR - Document Intelligence"])
