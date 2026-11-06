from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "منظومة الذكاء الاصطناعي لإدارة وتحليل الاحتياج الزكوي وتوجيه الموارد "
        "في الجمهورية اليمنية -- واجهة برمجة التطبيقات المؤسسية (Enterprise REST API)."
    ),
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS Middleware for Frontend Integration
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["الجذر - Root"])
def read_root():
    return {
        "system": settings.APP_NAME,
        "status": "online",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "description_ar": (
            "رشاد AI: منصة ويب مؤسسية لتحليل ودعم اتخاذ القرار الزكوي. "
            "المخرجات استرشادية وتخضع للمراجعة والاعتماد البشري."
        ),
    }
