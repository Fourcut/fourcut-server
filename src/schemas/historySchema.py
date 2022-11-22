from datetime import date
from typing import Optional

from pydantic import BaseModel


class HistoryCreate(BaseModel):
    studio_id: int
    title: str
    history_date: date


class HistoryUpdate(BaseModel):
    history_id: int  # 수정할 history의 id 이므로 required
    studio_id: int | None = None  # optiona
    title: str | None = None  # option

    class Config:
        orm_mode = True
