from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api import api_router
from .db import database
from .models import studioModel

studioModel.Base.metadata.create_all(database.engine)

app = FastAPI()  # instance

app.include_router(api_router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"msg": "hello world!"}


# @app.get("/studio/{studio_id}")
# def read_studio_by_id(studio_id: int, db: Session = Depends(get_db)):
#     db_studio = crud.get_studio_by_id(db, studio_id=studio_id)
#     print(db_studio)
#     return db_studio
