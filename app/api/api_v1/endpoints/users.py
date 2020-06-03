from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.otp import generate_random_otp
from app.api.utils.security import get_current_user
from app.core import config
from app.core.email import send_email_verify_otp
from app.crud.user import (
    create_user,
    get_by_email,
    get_by_id,
    update_user_info,
    user_email_verified,
)
from app.db_models.user import User as DBUser
from app.models.user import (
    EmailVerifyResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
    VerifyUserEmail,
)

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def register_user(
    *, db: Session = Depends(get_db), data: UserCreate, background_tasks: BackgroundTasks
):
    """registering new users."""
    otp = generate_random_otp()
    with expected_integrity_error(
        db, detail="There was a conflict with an existing user.", debug=False
    ):
        if user := create_user(db, user_in=data, otp=otp):
            background_tasks.add_task(send_email_verify_otp, user.email, user.otp)
    return user


@router.post("/users/verify_email", response_model=EmailVerifyResponse)
async def verify_user_email_otp(*, data: VerifyUserEmail, db: Session = Depends(get_db)):
    user = get_by_email(db, email=data.email)
    if user and (user.otp == data.otp):
        expiry_time = user.otp_created_at + timedelta(minutes=config.OTP_EXPIRY_MINUTES)
        if expiry_time >= datetime.utcnow():
            user = user_email_verified(db, user=user)
            if user.email_verified:
                return EmailVerifyResponse(
                    verified=True, message="Your email has been verified."
                )
    raise HTTPException(
        status_code=401, detail="Cannot verify your otp or it may have been expired."
    )


@router.get("/users", response_model=UserResponse)
async def get_user_details(
    *, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user),
):
    if user := get_by_id(db, user_id=current_user.id):
        return user
    raise HTTPException(status_code=404, detail="Can't find details of this user.")


@router.put("/users", response_model=UserResponse)
async def update_user(
    *,
    db: Session = Depends(get_db),
    data: UserUpdate,
    current_user: DBUser = Depends(get_current_user),
    background_tasks: BackgroundTasks,
):
    """If new `email` is found in data, email will no longer be
       verified and new OTP as well as OTP datetime will be generated.
    """
    otp = None
    if data.email and data.email != current_user.email:
        otp = generate_random_otp()
    with expected_integrity_error(
        db, detail="There was a conflict with an existing user.", debug=False
    ):
        if user := update_user_info(db, data=data, user=current_user, otp=otp):
            if otp and user.email:
                background_tasks.add_task(send_email_verify_otp, user.email, otp)
    return user
