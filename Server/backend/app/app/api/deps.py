from app.core.security import decode_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, sqlmodels
from app.core import security
from app.core.config import settings
from app.db.session import async_session
from app.db.session import SessionLocal
import logging
from typing import Generator, AsyncGenerator
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
token_auth = HTTPBearer()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def async_get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


async def get_current_gateway(
        db: AsyncSession = Depends(async_get_db), credentials: HTTPAuthorizationCredentials = Depends(token_auth)
) -> sqlmodels.Gateway:
    try:
        payload = decode_token(credentials.credentials)
        token_data = sqlmodels.GatewayTokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature is expired",
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    gateway: sqlmodels.Gateway = await crud.gateway.get(uuid=token_data.sub, db=db)
    if not gateway:
        raise HTTPException(status_code=404, detail="Gateway not found")
    return gateway


async def get_current_user(
        db: AsyncSession = Depends(async_get_db), token: str = Depends(reusable_oauth2)
) -> sqlmodels.User:
    try:
        payload = decode_token(token)
        token_data = sqlmodels.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user: sqlmodels.User = await crud.user.get(id=token_data.sub, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
        current_user: sqlmodels.User = Depends(get_current_user),
) -> sqlmodels.User:
    if not await crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
        current_user: sqlmodels.User = Depends(get_current_user),
) -> sqlmodels.User:
    if not await crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
