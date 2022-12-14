from typing import Optional

from pydantic import BaseModel


class FileCreate(BaseModel):
    history_id: int
    url: str

    class Config:
        orm_mode = True


class FileUpdate(BaseModel):
    file_id: int  # ์์ ํ  file์ id
    url: Optional[str] = None

    class Config:
        orm_mode = True
