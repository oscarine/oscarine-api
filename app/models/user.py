from datetime import datetime

from pydantic import AnyUrl, BaseModel, EmailStr, StrictBool


# Properties to be received during registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr = None
    name: str = None
    phone_number: str = None
    avatar_image: AnyUrl = None


class UserResponse(BaseModel):
    email: EmailStr
    name: str = None
    phone_number: str = None
    avatar_image: AnyUrl = None
    last_seen: datetime = None
    id: int
    email_verified: bool


class VerifyUserEmail(BaseModel):
    email: EmailStr
    otp: int


class EmailVerifyResponse(BaseModel):
    verified: StrictBool
    message: str
