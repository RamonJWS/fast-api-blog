from fastapi import Depends, APIRouter

from auth.authentication import get_current_active_user
from schemas import User

router = APIRouter(
    tags=["users"]
)


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
