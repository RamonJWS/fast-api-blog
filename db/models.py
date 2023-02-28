from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String

class DbBlog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    title = Column(String)
    content = Column(String)
