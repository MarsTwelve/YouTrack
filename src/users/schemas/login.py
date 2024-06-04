from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserInDB(BaseModel):
    hashed_password: str
