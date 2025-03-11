from fastapi import APIRouter
from app.api.endpoints import items_router

router = APIRouter()
router.include_router(items_router, prefix="/items", tags=["items"])