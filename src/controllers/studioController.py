from sqlalchemy.orm import Session

from ..services import studioService


def read_studio_by_id(studio_id: int, db: Session):
    return studioService.read_studio_by_id(db=db, studio_id=studio_id)


def read_studios_by_query(
    db: Session,
    latitude_start,
    latitude_end,
    longitude_start,
    longitude_end,
    company,
    search,
    favorite,
):
    return studioService.read_studios_by_query(
        db=db,
        latitude_start=latitude_start,
        latitude_end=latitude_end,
        longitude_start=longitude_start,
        longitude_end=longitude_end,
        company=company,
        search=search,
        favorite=favorite,
    )
