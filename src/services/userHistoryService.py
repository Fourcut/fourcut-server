from sqlalchemy.orm import Session

from ..models.models import UserHistory
from ..schemas.userHistorySchema import UserHistoryCreate, UserHistoryUpdate


def read_user_history(db: Session, user_history_id: int):
    return db.query(UserHistory).get(user_history_id)


# user id 로 userhistory 가져오기
def read_user_history_by_user_id(db: Session, user_id: int):
    return db.query(UserHistory).filter(UserHistory.user_id == user_id).all()


# history id 로 userhistory 가져오기
def read_user_history_by_history_id(db: Session, history_id: int):
    return db.query(UserHistory).filter(UserHistory.history_id == history_id).all()


def create_user_history(db: Session, user_history_body: UserHistoryCreate):
    db.add(user_history_body)
    db.commit()
    db.refresh(user_history_body)
    return user_history_body


# 유저히스토리의 유저id 또는 히스토리id 를 변경
def update_user_history(db: Session, user_history_body: UserHistoryUpdate):
    userHistory = db.query(UserHistory).get(user_history_body.history_id)
    if userHistory:
        if user_history_body.user_id:
            userHistory.user_id = user_history_body.user_id
        if user_history_body.history_id:
            userHistory.history_id = user_history_body.history_id
        db.commit()

    return userHistory


def delete_user_history(db: Session, user_history_id: int):
    userHistory = db.query(UserHistory).get(user_history_id)
    if userHistory:
        db.delete(userHistory)
        db.commit()
    return user_history_id
