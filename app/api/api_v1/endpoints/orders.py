from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.db_models.user import User
from app.models.order import CreateOrder

router = APIRouter()


@router.post("/orders")
async def create_new_order(
    *,
    db: Session = Depends(get_db),
    data: CreateOrder,
    current_user: User = Depends(get_current_user),
):
    return {"hello": "world"}
