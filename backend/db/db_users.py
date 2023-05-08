from datetime import datetime

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from db.models import DbUser
from schemas import NewUser
from auth.password import get_password_hash


def create_user(db: Session, request: NewUser):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=get_password_hash(request.password),
        created=datetime.utcnow().replace(microsecond=0)
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already exists")
    return new_user


def get_user(db: Session, user: str):
    return db.query(DbUser).filter(DbUser.username == user).first()
