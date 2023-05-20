from sqlalchemy import Column, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class DbBlog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    image_location = Column(String)
    username = Column(String, ForeignKey("users.username"))
    title = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)
    user = relationship("DbUser", back_populates="items")


class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    disabled = Column(Boolean, default=False)
    created = Column(DateTime)
    items = relationship("DbBlog", back_populates="user")

