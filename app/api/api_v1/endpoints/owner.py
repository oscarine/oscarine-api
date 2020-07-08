from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.otp import generate_random_otp
from app.api.utils.owner_security import get_current_owner
from app.core import config
from app.core.email import send_email_verify_otp
from app.core.jwt import create_access_token
from app.crud.owner import create_owner, get_by_id, update_owner_info
from app.db_models.owner import Owner as DBOwnerModel
from app.models.owner import OwnerCreate, OwnerDetails, OwnerUpdate
from app.models.token import Token

router = APIRouter()


@router.post("/owners", response_model=OwnerDetails, status_code=201)
async def register_owner(
    *,
    db: Session = Depends(get_db),
    data: OwnerCreate,
    background_tasks: BackgroundTasks,
    response: Response,
):
    """registering new owners."""
    otp = generate_random_otp()
    with expected_integrity_error(
        db, detail="There was a conflict with an existing owner.", debug=False
    ):
        if owner := create_owner(db, user_in=data, otp=otp):
            background_tasks.add_task(send_email_verify_otp, owner.email, owner.otp)
    response.status_code = status.HTTP_201_CREATED
    return owner


@router.get("/owners", response_model=OwnerDetails)
async def get_owner_details(
    *,
    db: Session = Depends(get_db),
    current_owner: DBOwnerModel = Depends(get_current_owner),
):
    if owner := get_by_id(db, owner_id=current_owner.id):
        return OwnerDetails(**jsonable_encoder(owner))
    raise HTTPException(status_code=404, detail="Can't find details of this owner.")


@router.patch("/owners", response_model=OwnerDetails)
async def update_owner(
    *,
    db: Session = Depends(get_db),
    data: OwnerUpdate,
    current_owner: DBOwnerModel = Depends(get_current_owner),
    background_tasks: BackgroundTasks,
):
    """If new `email` is found in data, email will no longer be
       verified and new OTP as well as OTP datetime will be generated.
    """
    otp = None
    if data.email and data.email != current_owner.email:
        otp = generate_random_otp()
    with expected_integrity_error(
        db, detail="There was a conflict with an existing owner", debug=False
    ):
        if owner := update_owner_info(db, data=data, owner=current_owner, otp=otp):
            if otp and owner.email:
                background_tasks.add_task(send_email_verify_otp, owner.email, otp)
    return owner
