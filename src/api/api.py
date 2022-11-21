from fastapi import APIRouter

from .routers import history, studio

api_router = APIRouter()

api_router.include_router(studio.router, prefix="/studio", tags=["studio"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
