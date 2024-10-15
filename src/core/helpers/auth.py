import os
from typing import Literal

from fastapi import HTTPException, Cookie
from pydantic import BaseModel, ValidationError
from jose import jwt, ExpiredSignatureError, JWTError

SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET")


class Session(BaseModel):
    id: str
    name: str
    email: str
    image: str
    role: Literal["STUDENT", "TEACHER", "LEADER", "ADMIN"]
    exp: int
    iat: int


def get_user(accessToken: str = Cookie(None)) -> Session:
    if accessToken is None:
        raise HTTPException(status_code=403, detail="Access token not found in cookies")

    try:
        payload = jwt.decode(accessToken, SECRET_KEY or "", algorithms=["HS256"])
    except ExpiredSignatureError as e:
        raise HTTPException(detail="shits expired", status_code=401) from e
    except JWTError as e:
        raise HTTPException(detail="invalid token", status_code=401) from e

    try:
        session = Session(**payload)
        if session.role == "STUDENT":
            raise HTTPException(detail="invalid token", status_code=401)
        return session
    except ValidationError as e:
        raise HTTPException(detail="invalid token", status_code=401) from e
