from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from secrets import SystemRandom
from datetime import datetime, timedelta
from app.models.user import UserCreate, UserUpdate, UserResponse, \
    EmailVerifyResponse, VerifyUserEmail
from app.crud.user import get_by_username, get_by_email, create_user, \
    get_by_id, update_user_info, user_email_verified

from sqlalchemy.orm import Session
from app.api.utils.db import get_db
from app.core.email import send_email_verify_otp
from app.core import config
from app.api.utils.security import get_current_user
from app.db_models.user import User as DBUser


router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def register_user(
    *,
    db: Session = Depends(get_db),
    data: UserCreate,
    background_tasks: BackgroundTasks
):
    """registering new users."""
    user = get_by_email(db, email=data.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists.",
        )
    otp = SystemRandom().randint(10000, 99999)
    user = create_user(db, user_in=data, otp=otp)
    background_tasks.add_task(send_email_verify_otp, data.email, otp)
    return UserResponse(**jsonable_encoder(user))


@router.post("/users/verify_email", response_model=EmailVerifyResponse)
async def verify_user_email_otp(
    *,
    data: VerifyUserEmail,
    db: Session = Depends(get_db)
):
    user = get_by_email(db, email=data.email)
    if user and (user.otp == data.otp):
        expiry_time = user.otp_created_at + \
            timedelta(minutes=config.OTP_EXPIRY_MINUTES)
        if expiry_time >= datetime.utcnow():
            user = user_email_verified(db, user=user)
            if user.email_verified:
                return EmailVerifyResponse(
                    verified=True,
                    message="Your email has been verified."
                )
    raise HTTPException(
        status_code=401,
        detail="Cannot verify your otp or it may have been expired."
    )


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
