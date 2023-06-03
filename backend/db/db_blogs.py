from db.models import DbBlog, DbUser
from schemas import BlogPost

from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from datetime import datetime


def create_blog(db: Session, request: BlogPost, username: str):
    try:
        request.image_metadata["path"]
    except KeyError:
        request.image_metadata["path"] = None

    new_blog = DbBlog(
        image_location=request.image_metadata["path"],
        username=username,
        title=request.title,
        content=request.content,
        timestamp=datetime.utcnow().replace(microsecond=0)
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def return_all_blogs(db: Session):
    return db.query(DbBlog).all()


def remove_blog(id: int, db: Session, username: str) -> str:
    blog = db.query(DbBlog)\
        .join(DbUser)\
        .filter(DbUser.username == username, DbBlog.id == id)\
        .first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} not found for user: {username}')
    db.delete(blog)
    db.commit()
    return f"deleted blog: {id}, title: {blog.title}"
