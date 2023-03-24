from backend.db.models import DbBlog
from backend.schemas import BlogPost

from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from datetime import datetime


def create_blog(db: Session, request: BlogPost):
    new_blog = DbBlog(
        image_url=request.image_url,
        username=request.user_name,
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


def return_all_image_urls(db: Session):
    return db.query(DbBlog).with_entities(DbBlog.image_url, DbBlog.id).all()

def remove_blog(id: int, db: Session):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id: {id} not found')
    db.delete(blog)
    db.commit()
    return f"deleted blog: {id}, title: {blog.title}"
