from typing import Optional

from pydantic import BaseModel


class FileCreate(BaseModel):
    history_id: int
    url: str

    class Config:
        orm_mode = True


class FileUpdate(BaseModel):
    file_id: int  # 수정할 file의 id
    url: Optional[str] = None

    class Config:
        orm_mode = True
