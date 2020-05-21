from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, EmailStr, StrictBool


class OwnerCreate(BaseModel):
    email: EmailStr
    password: str


class OwnerDetails(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    email: EmailStr
    last_seen: datetime
    id: int
    avatar_image: Optional[AnyUrl] = None
    email_verified: bool

    class Config:
        orm_mode = True


class OwnerUpdate(BaseModel):
    email: EmailStr = None
    name: str = None
    phone_number: str = None
    avatar_image: AnyUrl = None
    city: str = None
    state: str = None


class OwnerLogin(BaseModel):
    email: EmailStr
    password: str


class VerifyOwnerEmail(BaseModel):
    email: EmailStr
    otp: int


class OwnerEmailVerifyResponse(BaseModel):
    verified: StrictBool
    message: str
