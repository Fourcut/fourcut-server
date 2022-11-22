from sqlalchemy.orm import Session

from ..models.models import User


def read_user_by_id(db: Session, user_id: int):
    return db.query(User).get(user_id)


def read_user_by_clientid(db: Session, client_id: str):
    return db.query(User).filter(User.client_id == client_id).first()
