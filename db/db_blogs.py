from db.models import DbBlog
from schemas import BlogPost

from sqlalchemy.orm.session import Session


def create_blog(db: Session, request: BlogPost):
    new_blog = DbBlog(
        username=request.user_name,
        title=request.title,
        content=request.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def return_all_blogs(db: Session):
    return db.query(DbBlog).all()


def remove_blog(id: int, db: Session):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    db.delete(blog)
    db.commit()
    return f"deleted blog: {id}, title: {blog.title}"
