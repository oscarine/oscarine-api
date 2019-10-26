import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app.crud.user import get_by_id
from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.models.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user(
        token: str = Security(reusable_oauth2), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = get_by_id(db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found".format(token, payload, token_data)
        )
    return user
