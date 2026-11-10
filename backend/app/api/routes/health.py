from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "providers": {
            "ocr": settings.ocr_provider,
            "llm": settings.llm_provider,
            "llm_key_configured": bool(settings.gemini_api_key),
        },
    }

