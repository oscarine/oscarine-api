from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import create_access_token
from app.crud.auth import (
    get_owner_by_email,
    get_user_by_email,
    owner_authenticate,
    owner_email_verified,
    user_authenticate,
    user_email_verified,
)
from app.models.auth import EmailVerifyResponse, Login, VerifyEmail
from app.models.token import Token

router = APIRouter()


@router.post("/auth/owner/login", response_model=Token)
def owner_login_access_token(data: Login, db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login for owners, get an access token for future requests
    """
    owner = owner_authenticate(db, email=data.email, password=data.password)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"owner_id": owner.id}, expires_delta=access_token_expires
        )
    }


@router.post("/auth/user/login", response_model=Token)
def user_login_access_token(data: Login, db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_authenticate(db, email=data.email, password=data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )
    }


@router.post("/auth/owner/verify-email", response_model=EmailVerifyResponse)
async def verify_owner_email_otp(*, data: VerifyEmail, db: Session = Depends(get_db)):
    owner = get_owner_by_email(db, email=data.email)
    if owner and (owner.otp == data.otp):
        expiry_time = owner.otp_created_at + timedelta(
            minutes=config.OTP_EXPIRY_MINUTES
        )
        if expiry_time >= datetime.utcnow():
            owner = owner_email_verified(db, owner=owner)
            if owner.email_verified:
                return EmailVerifyResponse(
                    verified=True, message="Your email has been verified."
                )
    raise HTTPException(
        status_code=401, detail="Cannot verify your otp or it may have been expired."
    )


@router.post("/auth/user/verify-email", response_model=EmailVerifyResponse)
async def verify_user_email_otp(*, data: VerifyEmail, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=data.email)
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
