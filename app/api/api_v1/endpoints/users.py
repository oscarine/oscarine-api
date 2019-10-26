from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.models.user import UserCreate, UserUpdate, UserResponse
from app.crud.user import get_by_username, get_by_email, create_user, \
    get_by_id, update_user_info

from sqlalchemy.orm import Session
from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.db_models.user import User as DBUser


router = APIRouter()


@router.post("/users")
async def register_user(
    *,
    db: Session = Depends(get_db),
    data: UserCreate
):
    """registering new users."""
    user = get_by_username(db, username=data.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists.",
        )
    user = get_by_email(db, email=data.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists."
        )
    user = create_user(db, user_in=data)
    return user


@router.get("/users/{user_id}", response_model=UserResponse)
async def user_by_id(
    *,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_by_id(db, user_id=user_id)
    if user:
        # user found with the given user ID
        return UserResponse(**jsonable_encoder(user))
    # show exception otherwise
    raise HTTPException(
        status_code=404,
        detail="Can't find user with that user id"
    )


@router.put("/users")
async def update_user(
        *,
        db: Session = Depends(get_db),
        data: UserUpdate,
        current_user: DBUser = Depends(get_current_user)
):
    user = update_user_info(db, data=data, user=current_user)
    return user
