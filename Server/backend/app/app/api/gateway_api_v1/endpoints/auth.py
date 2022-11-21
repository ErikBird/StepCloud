from typing import Any, List
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, sqlmodels
from app.api import deps
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, sqlmodels
from app.core import security
from app.core.config import settings
from app.db.session import async_session
from app.db.session import SessionLocal
import logging

from typing import Generator, AsyncGenerator

router = APIRouter()


@router.post("/test-token", response_model=sqlmodels.Gateway)
async def test_token(current_gateway: sqlmodels.Gateway = Depends(deps.get_current_gateway)) -> Any:
    """
    Test access token
    """
    return current_gateway


@router.post("/refresh", response_model=sqlmodels.AccessToken)
async def refresh_access_token(current_gateway: sqlmodels.Gateway = Depends(deps.get_current_gateway)) -> Any:
    """
    Refresh access token
    """
    return sqlmodels.AccessToken(access_token=security.create_access_token(current_gateway.uuid))
