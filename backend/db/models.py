from sqlalchemy import Column, DateTime
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float
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
    user = relationship("DbUser", back_populates="blog")
    nsfw = relationship("DbNSFW", back_populates="blog")


class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    disabled = Column(Boolean, default=False)
    created = Column(DateTime)
    blog = relationship("DbBlog", back_populates="user")


class DbNSFW(Base):
    __tablename__ = "nsfw"
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    nsfw_prob = Column(Float)
    nsfw_flag = Column(Boolean)
    model_name = Column(String, unique=True)
    model_type = Column(String)
    blog = relationship("DbBlog", back_populates="nsfw")
