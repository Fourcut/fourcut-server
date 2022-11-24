from datetime import date

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ...controllers import historyController
from ...dependency.dbSession import get_db
from ...schemas.historySchema import HistoryCreate

router = APIRouter()  # /history
auth_scheme = HTTPBearer()


@router.get("/")
async def read_my_history_by_studioID(
    studio_id: int,
    db: Session = Depends(get_db),
    Authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return await historyController.read_my_history_by_studioID(
        db=db, studio_id=studio_id, Authorization=Authorization
    )


@router.get("/all")
async def read_my_all_history(
    db: Session = Depends(get_db),
    Authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return await historyController.read_my_all_histories(
        db=db, Authorization=Authorization
    )


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
    Authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    if Authorization:
        return await historyController.create_history(
            studio_id=studio_id,
            title=title,
            history_date=history_date,
            fileObj=fileObj,
            member_ids=member_ids,
            db=db,
            Authorization=Authorization,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="인증되지 않은 유저입니다"
        )


@router.get("/{history_id}")
async def read_history_by_historyID(
    history_id: int,
    db: Session = Depends(get_db),
    Authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return await historyController.read_history_by_historyID(
        db=db, history_id=history_id, Authorization=Authorization
    )


@router.get("/hashed/{hashed_history_id}")
def read_history_by_hashedID(
    hashed_history_id: str,
    db: Session = Depends(get_db),
):
    return historyController.read_history_by_hashedID(
        db=db, hashed_history_id=hashed_history_id
    )
