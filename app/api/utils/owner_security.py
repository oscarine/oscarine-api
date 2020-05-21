from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import jwt
from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.crud.owner import get_by_id
from app.models.token import OwnerTokenPayload
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/owner_login")


def get_current_owner(
    token: str = Security(reusable_oauth2), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = OwnerTokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    owner = get_by_id(db, owner_id=token_data.owner_id)
    if not owner:
        raise HTTPException(
            status_code=404, detail="Owner not found".format(token, payload, token_data)
        )
    return owner
