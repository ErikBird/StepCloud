from typing import Any, List
import logging
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, sqlmodels
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[sqlmodels.UserWithCustomer])
async def read_users(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users with customer information.
    """
    users = await crud.user.get_multi(db=db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(
            status_code=404,
            detail="No user in the system",
        )
    return users


@router.post("/", response_model=sqlmodels.User)
async def create_user(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        user_in: sqlmodels.UserCreate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(db=db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user
