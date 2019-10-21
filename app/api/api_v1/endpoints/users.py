from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate
from app.crud.user import get_by_username, get_by_email, create_user, \
    get_by_id

from sqlalchemy.orm import Session
from app.api.utils.db import get_db


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


@router.get("/users/{user_id}")
async def user_by_id(
    *,
    user_id: int,
    db: Session = Depends(get_db)
        ):
    user = get_by_id(db, user_id=user_id)
    if user:
        # user found with the given user ID
        return user
    # show exception otherwise
    raise HTTPException(
        status_code=404,
        detail="Can't find user with that user id"
    )
