from typing import Optional

from pydantic import BaseModel


class UserHistoryCreate(BaseModel):
    user_id: int
    history_id: str

    class Config:
        orm_mode = True


class UserHistoryUpdate(BaseModel):
    user_history_id: int  # 수정할 user_history의 id
    user_id: Optional[int] = None
    history_id: Optional[int] = None

    class Config:
        orm_mode = True
