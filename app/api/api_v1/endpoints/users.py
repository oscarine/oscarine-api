from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.otp import generate_random_otp
from app.api.utils.security import get_current_user
from app.core.email import send_email_verify_otp
from app.crud.user import create_user, update_user_info
from app.db_models.user import User as DBUser
from app.models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
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


@router.get("/users", response_model=UserResponse)
async def get_user_details(
    *,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    return current_user


@router.patch("/users", response_model=UserResponse)
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
