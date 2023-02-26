from pydantic import BaseModel


class BlogPost(BaseModel):
    user_name: str
    title: str
    content: str
