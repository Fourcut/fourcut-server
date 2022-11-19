from typing import Optional

from pydantic import BaseModel


class StudioBase(BaseModel):
    id: int
    company: str
    name: str
    address: str | None
    contact: str | None
    latitude: str
    longitude: str
    is_opened: bool

    class Config:
        orm_mode = True


class StudioQuery(BaseModel):
    latitude_start: float
    latitude_end: float
    longitude_start: float
    longitude_end: float
    company: Optional[str] = None
    search: Optional[str] = None
    favorite: Optional[bool] = None
