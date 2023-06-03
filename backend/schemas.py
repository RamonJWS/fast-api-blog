from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class BlogPost(BaseModel):
    image_metadata: Optional[Dict[str, Any]]
    title: str
    content: str


class DisplayBlogPost(BaseModel):
    id: int
    image_location: str | None
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


class ImageResponse(BaseModel):
    path: str
    nsfw_prob: float
    nsfw_flag: bool
    model_name: str
    class Config:
        orm_mode = True
