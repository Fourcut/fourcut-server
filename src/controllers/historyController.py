from typing import List, Optional

from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..models.models import File, History, User, UserHistory
from ..services import historyService, userHistoryService, userService


# 특정 사진관에서의 현재 유저의 히스토리 read
def read_history_by_studioID(db: Session, studio_id: int):

    ### 유저 임시 설정해놨음
    user_id = 1
    user = userService.read_user_by_id(db, user_id)
    #######

    triple_join_results = (
        db.query(History, UserHistory, File)
        .join(UserHistory, History.id == UserHistory.history_id)
        .join(File, History.id == File.history_id)
        .filter(History.studio_id == studio_id)
        .filter(UserHistory.user_id == user.id)
        .all()
    )

    result = []
    data = {}
    for history, user_history, file in triple_join_results:
        print(history)
        data["history"] = history
        data["files"] = []
        data["files"].append(file)

        data["members"] = []
        user_histories_by_history_id = (
            userHistoryService.read_user_history_by_history_id(db, history.id)
        )

        for userhistory in user_histories_by_history_id:
            data["members"].append(userhistory.user)

        result.append(data)

    return result


# 특정 사진관에서 현재 유저가 히스토리 생성
def create_history(
    title: str,
    files: Optional[List[UploadFile]],
    members: Optional[List[str]],
    db: Session,
):
    # body 에서 사진관 id 와 히스토리 제목, file, 멤버(자신포함) 받아옴

    pass
