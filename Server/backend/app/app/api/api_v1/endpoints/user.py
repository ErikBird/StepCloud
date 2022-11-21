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


@router.put("/me", response_model=sqlmodels.User)
async def update_user_me(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        user_in: sqlmodels.UserUpdate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = await crud.user.update(db=db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=sqlmodels.UserWithCustomer)
async def read_user_me(
        db: AsyncSession = Depends(deps.async_get_db),
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user with customer information.
    """

    return current_user


'''
@router.get("/{user_id}", response_model=sqlmodels.UserWithCustomer, tags=["User"])
async def read_user_by_id(
    user_id: int,
    current_user: sqlmodels.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.async_get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user: sqlmodels.User = await crud.user.get(db=db, id=int(user_id))
    if user == current_user:
        return user
    if not await crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="no user with the given id found",
        )
    return user


@router.put("/{user_id}", response_model=sqlmodels.User, tags=["User"])
async def update_user(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    user_id: int,
    user_in: sqlmodels.UserUpdate,
    current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return user
'''
