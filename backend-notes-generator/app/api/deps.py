import time
from typing import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config, security
from app.core.session import async_session
from app.models import User
from app.schemas.UserScheme import UserResponse
from app.core.security import JWTTokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(token: str = Depends(reusable_oauth2), db: AsyncSession = Depends(get_session)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=["HS256"])
        token_data = JWTTokenPayload(**payload)
    except jwt.JWTError:
        raise credentials_exception

    if int(time.time()) > token_data.expires_at:
        raise credentials_exception

    user = await db.get(User, token_data.subject)
    if not user:
        raise credentials_exception

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
    )
