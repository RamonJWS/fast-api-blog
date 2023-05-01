from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from auth.authentication import get_current_active_user
from schemas import User, NewUser, ResponseUser
from db.database import get_db
from db import db_users

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/create_account", response_model=ResponseUser)
async def create_account(user: NewUser, db: Session = Depends(get_db)):
    return db_users.create_user(db, user)
