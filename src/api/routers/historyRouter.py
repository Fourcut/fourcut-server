from datetime import date

from fastapi import APIRouter, Body, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from ...controllers import historyController
from ...dependency.dbSession import get_db
from ...schemas.historySchema import HistoryCreate

router = APIRouter()  # /history


@router.get("/")
def read_history_by_studioID(studio_id: int, db: Session = Depends(get_db)):
    return historyController.read_history_by_studioID(db=db, studio_id=studio_id)


# request 가 multipart-form 으로 넘어오기 때문에 pydantic schema 로 validation 불가
@router.post("/")
async def create_history(
    studio_id: int = Form(),
    title: str = Form(),
    history_date: date | None = Form(default=None),
    fileObj: UploadFile | None = File(),
    member_ids: list[int]
    | None = Query(
        default=None
    ),  # member_id 는 쿼리로! (fastapi 에서 form 을 보낼 때는 body 에 list 를 못 담음)
    db: Session = Depends(get_db),
):
    return historyController.create_history(
        studio_id=studio_id,
        title=title,
        history_date=history_date,
        fileObj=fileObj,
        member_ids=member_ids,
        db=db,
    )
