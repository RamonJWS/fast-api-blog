from db.database import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql.sqltypes import Integer, String

class DbBlog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, default="http://127.0.0.1:8000/files/no_image.png")
    username = Column(String)
    title = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)
