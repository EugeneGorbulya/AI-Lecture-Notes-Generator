"""Security module for JWT token generation and password hashing."""
import time
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
from app.core import config
from app.schemas.UserScheme import AuthSchemeAccessTokenResponse

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECS = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_TOKEN_EXPIRE_SECS = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTTokenPayload(BaseModel):
    subject: Union[str, int]
    refresh: bool
    issued_at: int
    expires_at: int

def create_jwt_token(exp_secs: int, refresh: bool, **kwargs):
    issued_at = int(time.time())
    expires_at = issued_at + exp_secs

    payload = {
        "issued_at": issued_at,
        "expires_at": expires_at,
        "refresh": refresh,
        **kwargs
    }

    token = jwt.encode(
        payload,
        key=config.settings.SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return token, expires_at, issued_at

def generate_access_token_response(role: str, **kwargs):
    access_token, expires_at, issued_at = create_jwt_token(
        exp_secs=ACCESS_TOKEN_EXPIRE_SECS, refresh=False, **kwargs
    )
    refresh_token, refresh_expires_at, refresh_issued_at = create_jwt_token(
        exp_secs=REFRESH_TOKEN_EXPIRE_SECS, refresh=True, **kwargs
    )
    return AuthSchemeAccessTokenResponse(
        token_type="Bearer",
        access_token=access_token,
        expires_at=expires_at,
        issued_at=issued_at,
        refresh_token=refresh_token,
        refresh_token_expires_at=refresh_expires_at,
        refresh_token_issued_at=refresh_issued_at,
        role=role
    )

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
