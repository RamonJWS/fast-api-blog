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
    image_url: Union[str, None]
    username: str
    title: str
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
