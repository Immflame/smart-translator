from fastapi import APIRouter
from .translation.routes import router as translation_router

router = APIRouter()
router.include_router(translation_router)
