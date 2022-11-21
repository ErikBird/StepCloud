import logging
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.get("/me", response_model=List[sqlmodels.CustomerDeviceReadWithDevice])
async def read_device_customer_me(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve my device-customer
    """
    device_customer = await crud.customer_device.get_multi_by_customer(db, customer_id=current_user.customer_id,
                                                                       skip=skip,
                                                                       limit=limit)
    return device_customer


@router.post("/me", response_model=sqlmodels.CustomerDeviceRead)
async def create_device_customer_me(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        device_customer_in: sqlmodels.CustomerDeviceCreate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new device-customer for owner.
    """
    device_customer = await crud.customer_device.create_with_customer(db, obj_in=device_customer_in,
                                                                      db_obj=current_user)
    return device_customer


@router.put("/{device_customer_id}", response_model=sqlmodels.CustomerDeviceRead)
async def update_device_customer(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        device_customer_id: int,
        device_customer_in: sqlmodels.CustomerDeviceUpdate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a device customer.
    """
    device_customer = await crud.customer_device.get(db, id=device_customer_id)
    if not device_customer:
        raise HTTPException(
            status_code=404,
            detail="The device_customer with this id does not exist in the system",
        )
    if not current_user.customer_id == device_customer.customer_id:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    device_customer = await crud.user.update(db, db_obj=device_customer, obj_in=device_customer_in)
    return device_customer
