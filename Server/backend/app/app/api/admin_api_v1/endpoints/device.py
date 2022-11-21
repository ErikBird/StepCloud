from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[sqlmodels.DeviceReadWithRelationships])
async def read_device(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve devices.
    """
    devices = await crud.device.get_multi_with_identifier(db, skip=skip, limit=limit)
    return devices


@router.get("/by-identifier/{expression}", response_model=sqlmodels.DeviceReadWithRelationships)
async def read_device(
        expression: str,
        db: AsyncSession = Depends(deps.async_get_db),
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    device = await crud.device.get_by_identifier(db, expression=expression)
    if not device:
        raise HTTPException(
            status_code=404,
            detail="No device with this identifier found",
        )

    return device
