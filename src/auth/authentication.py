from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from src.users.schemas.login import UserLogin
from src.auth.schemas import TokenData

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "1efedc77f68e059b7c78dcbcc9d7b9007f6597e44edcf9cb1f53c1b75387d4c5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def get_token_timedelta():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(user_login: UserLogin, user_in_db):
    if not verify_password(user_login.password, user_in_db["hashed_password"]):
        return False
    return user_login


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload_data: str = payload.get("sub")
        if payload_data is None:
            raise
        token_data = TokenData(payload_data=payload_data)
    except InvalidTokenError:
        return False
    return token_data
