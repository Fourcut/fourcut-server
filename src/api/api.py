from fastapi import APIRouter

from .routers import studio

api_router = APIRouter()

api_router.include_router(studio.router, prefix="/studio", tags=["studio"])
