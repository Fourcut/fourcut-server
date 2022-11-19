from fastapi import FastAPI

from .db import database, models

models.Base.metadata.create_all(database.engine)

app = FastAPI()  # instance


@app.get("/")
def root():
    return {"msg": "hello world!"}
