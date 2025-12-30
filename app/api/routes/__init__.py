from fastapi import APIRouter
from app.api.routes.data import router as data_router

router = APIRouter()
router.include_router(data_router)
