from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.token import Token
from app.models.user import UserLogin
from app.api.utils.db import get_db
from app.crud.user import authenticate
from app.core import config
from app.core.jwt import create_access_token

from datetime import timedelta


router = APIRouter()


@router.post("/login", response_model=Token, tags=["login"])
def login_access_token(
        data: UserLogin,
        db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        db, email=data.email, password=data.password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )
    }
