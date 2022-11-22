from fastapi import APIRouter

from .routers import historyRouter, oauthRouter, studioRouter

api_router = APIRouter()

api_router.include_router(studioRouter.router, prefix="/studio", tags=["studio"])
api_router.include_router(historyRouter.router, prefix="/history", tags=["history"])
api_router.include_router(oauthRouter.router, prefix="/oauth", tags=["oauth"])
