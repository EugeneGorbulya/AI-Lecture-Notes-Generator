from app.schemas.BaseScheme import BaseScheme, str_big_factory
from pydantic import EmailStr
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseScheme):
    email: EmailStr = str_big_factory()
    username: str = str_big_factory()

class UserCreate(UserBase):
    password: str = str_big_factory()

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

class AuthSchemeAccessTokenResponse(BaseScheme):
    token_type: str
    access_token: str
    refresh_token: str
    expires_at: int
    issued_at: int
    refresh_token_expires_at: int
    refresh_token_issued_at: int
    role: str
