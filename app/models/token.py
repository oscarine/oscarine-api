from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    user_id: int = None


class OwnerTokenPayload(BaseModel):
    owner_id: int = None
