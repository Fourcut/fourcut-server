from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api import api_router
from .db.database import Base, engine

Base.metadata.create_all(engine)


app = FastAPI(
    title="nemo API v1",
    version="0.0.1",
)  # instance

app.include_router(api_router)


origins = ["http://localhost:3000", "http://ne-mo.me", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
