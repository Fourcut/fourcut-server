from sqlalchemy.orm import Session

from ..models.models import File
from ..schemas.fileSchema import FileCreate, FileUpdate


def read_file(db: Session, file_id: int):
    return db.query(File).get(file_id)


def create_file(db: Session, file_body: FileCreate):
    db.add(file_body)
    db.commit()
    db.refresh(file_body)
    return file_body


# file url만 변경가능
def update_file(db: Session, file_body: FileUpdate):
    file = db.query(File).get(file_body.file_id)
    if file and file_body.url:
        file.url = file_body.url
        db.commit()

    return file


def delete_file(db: Session, file_id: int):
    file = db.query(File).get(file_id)
    if file:
        db.delete(file)
        db.commit()
    return file_id
