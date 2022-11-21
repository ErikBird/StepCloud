import logging
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.get("/customers/{customer_id}/devices", response_model=List[sqlmodels.CustomerDeviceRead])
async def read_device_customer(
        customer_id: int,
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve device customer by customer id.
    """
    device_customer = await crud.customer_device.get_multi_by_customer(db, customer_id=customer_id, skip=skip,
                                                                       limit=limit)
    if not await crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return device_customer
