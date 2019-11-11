from pydantic import BaseModel
from pydantic.types import EmailStr

from typing import Optional


class OwnerCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class OwnerDetails(BaseModel):
    username: str
    state: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    id: int
    avatar_image: Optional[str] = None

    class Config:
        orm_mode = True


class OwnerUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    avatar_image: str = None
    city: str = None
    state: str = None


class OwnerLogin(BaseModel):
    username: str
    password: str
