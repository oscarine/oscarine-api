from datetime import datetime, timedelta
from secrets import SystemRandom

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.owner_security import get_current_owner
from app.core import config
from app.core.email import send_email_verify_otp
from app.core.jwt import create_access_token
from app.crud.owner import (
    authenticate,
    create_owner,
    get_by_email,
    get_by_id,
    owner_email_verified,
    update_owner_info,
)
from app.db_models.owner import Owner as DBOwnerModel
from app.models.owner import (
    OwnerCreate,
    OwnerDetails,
    OwnerEmailVerifyResponse,
    OwnerLogin,
    OwnerUpdate,
    VerifyOwnerEmail,
)
from app.models.token import Token

router = APIRouter()


@router.post("/owners", response_model=OwnerDetails)
async def register_owner(
    *, db: Session = Depends(get_db), data: OwnerCreate, background_tasks: BackgroundTasks
):
    """registering new owners."""
    otp = SystemRandom().randint(10000, 99999)
    with expected_integrity_error(
        db, detail="There was a conflict with an existing user", debug=False
    ):
        owner = create_owner(db, user_in=data, otp=otp)
    if owner is not None:
        background_tasks.add_task(send_email_verify_otp, data.email, otp)
    return owner


@router.post("/owners/verify_email", response_model=OwnerEmailVerifyResponse)
async def verify_owner_email_otp(
    *, data: VerifyOwnerEmail, db: Session = Depends(get_db)
):
    owner = get_by_email(db, email=data.email)
    if owner and (owner.otp == data.otp):
        expiry_time = owner.otp_created_at + timedelta(minutes=config.OTP_EXPIRY_MINUTES)
        if expiry_time >= datetime.utcnow():
            owner = owner_email_verified(db, owner=owner)
            if owner.email_verified:
                return OwnerEmailVerifyResponse(
                    verified=True, message="Your email has been verified."
                )
    raise HTTPException(
        status_code=401, detail="Cannot verify your otp or it may have been expired."
    )


@router.get("/owners", response_model=OwnerDetails)
async def get_owner_details(
    *,
    db: Session = Depends(get_db),
    current_owner: DBOwnerModel = Depends(get_current_owner),
):
    if owner := get_by_id(db, owner_id=current_owner.id):
        return OwnerDetails(**jsonable_encoder(owner))
    raise HTTPException(status_code=404, detail="Can't find details of this owner.")


@router.post("/owner_login", response_model=Token, tags=["owner", "login"])
def owner_login_access_token(data: OwnerLogin, db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login for owners, get an access token for future requests
    """
    owner = authenticate(db, email=data.email, password=data.password)
    if not owner:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"owner_id": owner.id}, expires_delta=access_token_expires
        )
    }


@router.put("/owners", response_model=OwnerDetails)
async def update_owner(
    *,
    db: Session = Depends(get_db),
    data: OwnerUpdate,
    current_owner: DBOwnerModel = Depends(get_current_owner),
):
    with expected_integrity_error(
        db, detail="There was a conflict with an existing owner", debug=False
    ):
        owner = update_owner_info(db, data=data, owner=current_owner)
    return owner
