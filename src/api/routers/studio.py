from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...controllers import studioController
from ...dependency.dbSession import get_db
from ...schemas import studioSchema

router = APIRouter()  # /studio


@router.get("/{studio_id}", response_model=studioSchema.StudioBase)
def read_studio_by_id(studio_id: int, db: Session = Depends(get_db)):
    return studioController.read_studio_by_id(db=db, studio_id=studio_id)


@router.get("/", response_model=List[studioSchema.StudioBase])
def read_studio_by_query(
    latitude_start: float | None = Query(default=None),
    latitude_end: float | None = Query(default=None),
    longitude_start: float | None = Query(default=None),
    longitude_end: float | None = Query(default=None),
    company: str | None = Query(default=None),
    search: str | None = Query(default=None),
    favorite: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return studioController.read_studios_by_query(
        db=db,
        latitude_start=latitude_start,
        latitude_end=latitude_end,
        longitude_start=longitude_start,
        longitude_end=longitude_end,
        company=company,
        search=search,
        favorite=favorite,
    )
