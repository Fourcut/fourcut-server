import os
from datetime import date, datetime

from fastapi import File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..dependency.s3Auth import s3_auth
from ..models.models import File, History, User, UserHistory
from ..s3.s3Upload import upload_file_to_bucket
from ..services import (
    fileService,
    historyService,
    studioService,
    userHistoryService,
    userService,
)


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

    # return triple_join_results

    result = []
    for history, user_history, file in triple_join_results:
        data = {}
        data["history"] = history
        data["files"] = []
        data["files"].append(file)

        data["members"] = []
        user_histories_by_history_id = (
            userHistoryService.read_user_history_by_history_id(db, history.id)
        )

        for userhistory in user_histories_by_history_id:
            data["members"].append(userhistory.user)

        print(data["history"].__dict__)

        result.append(data)

    return result


# 특정 사진관에서 현재 유저가 히스토리 생성
def create_history(
    *,
    studio_id: int,
    title: str,
    history_date: date | None = None,
    fileObj: UploadFile | None = None,
    member_ids: list[int] | None = None,
    db: Session,
):
    # history 생성 <= studio_id, title, history_date 집어넣기
    if history_date is None:
        history_date = date.today()
    historyObj = History(studio_id, title, history_date)

    db.add(historyObj)
    db.flush()

    # # history id 얻기
    historyObj_id = historyObj.id

    # members 단위로 user_history 객체생성해서 user_histories 넣어주기

    ######## TODO #########
    user_id = 1  ###### user_id 임시설정!! 나중에 지우기
    ######################

    userHistoryObj = UserHistory(user_id, historyObj_id)
    historyObj.user_histories = [userHistoryObj]
    # 위 문장은 db.add(userHistoryObj) 랑 같은 효과임
    # historyObj add 다시 필요한가? => NO

    if member_ids is not None:
        for member_id in member_ids:
            userHistoryObj = UserHistory(member_id, historyObj_id)
            historyObj.user_histories.append(userHistoryObj)
            # 위 문장은 db.add(userHistoryObj) 랑 같은 효과임
            # historyObj add 다시 필요한가? => NO. ORM 이 알아서 해줌

    # file 객체 만들어서 files 에 넣어주기

    if fileObj is not None:
        # s3 필요
        s3 = s3_auth()

        filename = fileObj.filename
        current_time = datetime.now()
        split_file_name = os.path.splitext(
            filename
        )  # split the file name into two different path (string + extention)
        file_name_unique = str(current_time.timestamp()).replace(
            ".", ""
        )  # for realtime application you must have genertae unique name for the file
        file_extension = split_file_name[1]  # file extention
        object_name = file_name_unique + "_" + split_file_name[0] + file_extension

        try:
            bucket = "nemo-storage"
            folder = "files"
            upload_obj = upload_file_to_bucket(
                s3_client=s3,
                file_obj=fileObj.file,
                bucket=bucket,
                folder=folder,
                object_name=object_name,
            )

            file_url = f"https://{bucket}.s3.ap-northeast-2.amazonaws.com/{folder}/{object_name}"

            new_file = File(history_id=historyObj_id, url=file_url)
            historyObj.files = [new_file]

            db.commit()

            return {
                "content": "Object has been uploaded to bucket successfully",
                "created_history_id": historyObj.id,
            }

        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="File could not be uploaded",
            )


def read_history_by_historyID(history_id: int, db: Session):

    # 해당 유저에 대한 인증 필요
    # TODO
    user_id = 1  # 임시 설정
    #### 수정필요

    try:
        userHistoryObj = (
            db.query(UserHistory).filter(UserHistory.history_id == history_id).first()
        )
        if userHistoryObj.user_id != user_id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content="유저의 히스토리가 아닙니다"
            )

        # response 할 데이터 : 사진관, 히스토리, 파일들, 유저목록
        historyObj = historyService.read_history(db=db, history_id=history_id)

        studioObj = studioService.get_studio_by_id(db, historyObj.studio_id)
        fileObj = db.query(File).filter(File.history_id == history_id).all()

        memberObjs = (
            db.query(UserHistory, User)
            .join(User, UserHistory.user_id == User.id)
            .filter(UserHistory.history_id == history_id)
            .all()
        )

        members = []
        for uh, userObj in memberObjs:
            members.append(userObj)

        return {
            "history": historyObj,
            "studio": studioObj,
            "files": fileObj,
            "members": members,
        }

    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="잘못된 요청입니다"
        )
