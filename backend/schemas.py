from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union


class BlogPost(BaseModel):
    user_name: str
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