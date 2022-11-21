from typing import List, Optional

from fastapi import APIRouter, Body, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ...controllers import historyController
from ...dependency.dbSession import get_db
from ...schemas import studioSchema

router = APIRouter()  # /history


@router.get("/")
def read_history_by_studioID(studio_id: int, db: Session = Depends(get_db)):
    return historyController.read_history_by_studioID(db=db, studio_id=studio_id)


# @router.post("/")
# async def create_history(
#     title: str = Body(),
#     files: Optional[List[UploadFile]] = File(None),
#     members: Optional[List[str]] = None,
#     db: Session = Depends(get_db),
# ):
#     return historyController.create_history
