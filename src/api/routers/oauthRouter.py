import json
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, Header, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ...controllers import oauthController
from ...dependency.dbSession import get_db
from ...services.userService import read_user_by_clientid

router = APIRouter()  # /oauth
auth_scheme = HTTPBearer()


@router.post("/kakao")
async def kakaoAuth(
    response: Response,
    kakao_access_token: dict = Body(),
    db: Session = Depends(get_db),
):
    try:
        get_user_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": "Bearer " + kakao_access_token["access_token"]}
        userdata = requests.post(url=get_user_url, headers=headers)

        _userdata = userdata.json()

        access_token = oauthController.create_access_token(db, _userdata)

        response.status_code = status.HTTP_201_CREATED
        return {"access_token": access_token, "token_type": "bearer"}

    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "인증에 실패했습니다"}


@router.get("/user")
async def get_authenticated_user(
    response: Response,
    db: Session = Depends(get_db),
    Authorization: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    if Authorization:
        response.status_code = status.HTTP_202_ACCEPTED
        return await oauthController.get_current_user(
            db=db, token=Authorization.credentials
        )
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "인증되지 않았습니다"}
