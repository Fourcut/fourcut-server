from fastapi import APIRouter

from .routers import historyRouter, studioRouter

api_router = APIRouter()

api_router.include_router(studioRouter.router, prefix="/studio", tags=["studio"])
api_router.include_router(historyRouter.router, prefix="/history", tags=["history"])
