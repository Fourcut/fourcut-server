from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from db import database, models

app = FastAPI()  # instance

models.Base.metadata.create_all(database.engine)
