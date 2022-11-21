from sqlalchemy.orm import Session

from ..models import models


def read_user_by_id(db: Session, user_id: int):
    return db.query(models.User).get(user_id)
