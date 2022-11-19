from sqlalchemy import Float, cast, or_
from sqlalchemy.orm import Session

from ..models import studioModel


def get_studio_by_id(db: Session, studio_id: int):
    return (
        db.query(studioModel.Studio).filter(studioModel.Studio.id == studio_id).first()
    )


def get_studios_by_query(
    db: Session,
    latitude_start,
    latitude_end,
    longitude_start,
    longitude_end,
    company,
    search,
    favorite,
):
    print(company)
    result = (
        db.query(studioModel.Studio)
        .filter(
            latitude_start <= cast(studioModel.Studio.latitude, Float()),
            cast(studioModel.Studio.latitude, Float()) <= latitude_end,
        )
        .filter(
            longitude_start <= cast(studioModel.Studio.longitude, Float()),
            cast(studioModel.Studio.longitude, Float()) <= longitude_end,
        )
    )

    if company:
        result = result.filter(studioModel.Studio.company == company)
    if search:
        convert_keyword = "%{}%".format(search)
        result = result.filter(
            or_(
                studioModel.Studio.company.like(convert_keyword),
                studioModel.Studio.name.like(convert_keyword),
            )
        )
    if favorite:
        pass  # TODO

    return result.all()
