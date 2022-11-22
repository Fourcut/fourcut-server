from sqlalchemy import Float, cast, or_
from sqlalchemy.orm import Session

from ..models import models


def read_studio_by_id(db: Session, studio_id: int):
    return db.query(models.Studio).filter(models.Studio.id == studio_id).first()


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
    result = db.query(models.Studio)
    if latitude_start and latitude_end and longitude_start and longitude_end:
        result = result.filter(
            latitude_start <= cast(models.Studio.latitude, Float()),
            cast(models.Studio.latitude, Float()) <= latitude_end,
        ).filter(
            longitude_start <= cast(models.Studio.longitude, Float()),
            cast(models.Studio.longitude, Float()) <= longitude_end,
        )

    if company:
        result = result.filter(models.Studio.company == company)
    if search:
        convert_keyword = "%{}%".format(search)
        result = result.filter(
            or_(
                models.Studio.company.like(convert_keyword),
                models.Studio.name.like(convert_keyword),
                models.Studio.address.like(convert_keyword),
            )
        )
    if favorite:
        pass  # TODO

    return result.all()
