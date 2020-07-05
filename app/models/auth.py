from pydantic import BaseModel, EmailStr, StrictBool


class Login(BaseModel):
    email: EmailStr
    password: str


class VerifyEmail(BaseModel):
    email: EmailStr
    otp: int


class EmailVerifyResponse(BaseModel):
    verified: StrictBool
    message: str
