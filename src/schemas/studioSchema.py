from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CompanyName(str, Enum):
    인생네컷 = "인생네컷"
    포토그레이 = "포토그레이"
    포토시그니처 = "포토시그니처"
    포토이즘 = "포토이즘"
    하루필름 = "하루필름"


class StudioBase(BaseModel):
    id: int
    company: CompanyName
    name: str
    address: str | None
    contact: str | None
    latitude: str
    longitude: str
    is_opened: bool

    class Config:
        orm_mode = True


# class StudioQuery(BaseModel):
#     latitude_start: float
#     latitude_end: float
#     longitude_start: float
#     longitude_end: float
#     company: CompanyName | None = None
#     search: Optional[str] = None
#     favorite: Optional[bool] = None
