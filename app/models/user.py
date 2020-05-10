from pydantic import BaseModel, EmailStr


# Properties to be received during registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str = None
    email: str = None
    bio: str = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    avatar_image: str = None
    city: str = None
    state: str = None


class UserResponse(BaseModel):
    username: str = None
    email: str = None
    bio: str = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    avatar_image: str = None
    city: str = None
    state: str = None
    role: str = None
    last_seen: str = None
    id: int = None
