from sqlalchemy.orm import Session

from ..models.models import History
from ..schemas.historySchema import HistoryCreate, HistoryUpdate


def read_history(db: Session, history_id: int):
    return db.query(History).get(history_id)


def create_history(db: Session, history_body: HistoryCreate):
    db.add(history_body)
    db.commit()
    db.refresh(history_body)
    return history_body


# 여기서는 history title만 변경가능
def update_history(db: Session, history_body: HistoryUpdate):
    history = db.query(History).get(history_body.history_id)
    if history and history_body.title:
        history.title = history_body.title
        db.commit()

    return history


def delete_history(db: Session, history_id: int):
    history = db.query(History).get(history_id)
    if history:
        db.delete(history)
        db.commit()
    return history_id
