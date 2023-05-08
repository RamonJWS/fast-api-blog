from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BlogPost(BaseModel):
    image_url: Optional[str]
    title: str
    content: str


class DisplayBlogPost(BaseModel):
    id: int
    image_url: str | None
    username: str
    title: str
    content: str
    timestamp: datetime
    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class NewUser(BaseModel):
    username: str
    email: str
    password: str


class ResponseUser(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
