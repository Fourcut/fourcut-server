import json
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ...controllers import oauthController
from ...dependency.dbSession import get_db
from ...services.userService import read_user_by_clientid

router = APIRouter()  # /oauth

load_dotenv()

KAKAO_RESTAPI_KEY = os.environ.get("KAKAO_RESTAPI_KEY")
REDIRECT_URI = os.environ.get("REDIRECT_URI")


@router.get("/kakao")
def kakaoClient():
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_RESTAPI_KEY}&response_type=code&redirect_uri={REDIRECT_URI}"

    response = RedirectResponse(url)
    return response


@router.get("/kakao/redirect")
async def kakaoAuth(
    response: Response,
    code: str | None = "",
    db: Session = Depends(get_db),
):
    try:
        _url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_RESTAPI_KEY}&code={code}&redirect_uri={REDIRECT_URI}"
        _res = requests.post(_url)  # kakao token
        _result = _res.json()  # kakao token
        response.set_cookie(key="kakao", value=str(_result["access_token"]))

        get_user_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": "Bearer " + _result["access_token"]}
        userdata = requests.post(url=get_user_url, headers=headers)

        _userdata = userdata.json()

        access_token = oauthController.create_access_token(db, _userdata)

        response.status_code = status.HTTP_201_CREATED
        return {"access_token": access_token, "token_type": "bearer"}

    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "인증에 실패했습니다"}


@router.get("/kakao/logout")
def kakaoLogout(request: Request, response: Response):
    url = "https://kapi.kakao.com/v1/user/unlink"
    KEY = request.cookies["kakao"]
    headers = dict(Authorization=f"Bearer {KEY}")
    _res = requests.post(url, headers=headers)
    response.set_cookie(key="kakao", value=None)
    response.status_code = status.HTTP_200_OK
    return {"logout": _res.json()}
