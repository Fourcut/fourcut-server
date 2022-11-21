from typing import Optional

from pydantic import BaseModel

 # body 에서 사진관 id 와 히스토리 제목, file, 멤버(자신포함) 받아옴
class HistoryCreate(BaseModel):
    studio_id: int
    title: str
    

    class Config:
        orm_mode = True


class HistoryUpdate(BaseModel):
    history_id: int  # 수정할 history의 id
    studio_id: Optional[int] = None
    title: Optional[str] = None

    class Config:
        orm_mode = True



 
 