from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.crud.owner import get_by_id
from app.models.token import OwnerTokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/owner_login")


def get_current_owner(
    token: str = Security(reusable_oauth2), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        owner_id: int = payload.get("owner_id")
        if owner_id is None:
            raise credentials_exception
        token_data = OwnerTokenPayload(owner_id=owner_id)
    except JWTError:
        raise credentials_exception
    owner = get_by_id(db, owner_id=token_data.owner_id)
    if owner is None:
        raise credentials_exception
    return owner
