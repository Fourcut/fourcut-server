import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..models.models import User
from ..services import userService

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(db: Session, userdata: dict):
    # user 의 client id 를 db 에서 조회
    client_id = userdata["id"]
    db_user = userService.read_user_by_clientid(db, client_id)
    kakao_account = userdata["kakao_account"]

    # db 에 없으면 유저 생성 후 userid 얻어옴
    if db_user is None:
        if "email" not in kakao_account:
            email = None
        else:
            email = kakao_account["email"]
            name = kakao_account["profile"]["nickname"]
            avatar = kakao_account["profile"]["thumbnail_image_url"]
            new_user = User(
                client_id=userdata["id"],
                email=email,
                name=name,
                avatar=avatar,
                is_member=True,
            )
            db.add(new_user)
            db.flush()
            uid = new_user.id
            db.commit()
    else:
        uid = db_user.id
        email = db_user.email

    token = {"user_id": uid, "client_id": client_id, "email": email}

    # 토큰 생성
    encoded_jwt = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
