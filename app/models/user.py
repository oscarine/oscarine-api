from pydantic import BaseModel
from pydantic.types import EmailStr


# Properties to be received during registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
