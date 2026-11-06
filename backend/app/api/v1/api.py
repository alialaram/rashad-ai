from fastapi import APIRouter
from app.api.v1.endpoints import health

api_router = APIRouter()

# مسار فحص صحة النظام
api_router.include_router(health.router, prefix="/health", tags=["الصحة والمراقبة - Health"])
