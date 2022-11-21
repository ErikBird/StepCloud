from typing import Any, List
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, sqlmodels
from app.api import deps
import logging

router = APIRouter()


@router.get("/{customer_device_id}/events", response_model=List[sqlmodels.DeviceEventWithType])
async def read_device_events(
        customer_device_id: int,
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    if await crud.user.is_superuser(current_user):
        device_event = await crud.device_event.get_multi_by_id(db, customer_device_id=customer_device_id, skip=skip,
                                                               limit=limit)
    else:
        devicecustomer = await crud.customer_device.get_by_id(db=db, id=customer_device_id)
        if not devicecustomer:
            raise HTTPException(status_code=404, detail="Device-Customer not found")
        if devicecustomer.customer_id != current_user.customer_id:
            raise HTTPException(status_code=400, detail="You can only read Log Data for your own devices!")
        device_event = await crud.device_event.get_multi_by_id(db, customer_device_id=customer_device_id, skip=skip,
                                                               limit=limit)
    return device_event


@router.get("/{customer_device_id}/events/last", response_model=sqlmodels.DeviceEventWithData)
async def read_last_device_event(
        customer_device_id: int,
        db: AsyncSession = Depends(deps.async_get_db),
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    if await crud.user.is_superuser(current_user):
        device_event = await crud.device_event.get_last(db, customer_device_id=customer_device_id)
    else:
        devicecustomer = await crud.customer_device.get_by_id(db=db, id=customer_device_id)
        if not devicecustomer:
            raise HTTPException(status_code=404, detail="Device-Customer not found")
        if devicecustomer.customer_id != current_user.customer_id:
            raise HTTPException(status_code=400, detail="You can only read Log Data for your own Devices!")
        device_event = await crud.device_event.get_last(db, customer_device_id=customer_device_id)
    return device_event


@router.get("/{customer_device_id}/events/{event_id}", response_model=sqlmodels.DeviceEventWithData)
async def read_last_device_event(
        customer_device_id: int,
        event_id: int,
        db: AsyncSession = Depends(deps.async_get_db),
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    if await crud.user.is_superuser(current_user):
        device_event = await crud.device_event.get_by_id(db, customer_device_id=customer_device_id, event_id=event_id)
    else:
        devicecustomer = await crud.customer_device.get_by_id(db=db, id=customer_device_id)
        if not devicecustomer:
            raise HTTPException(status_code=404, detail="Device-Customer not found")
        if devicecustomer.customer_id != current_user.customer_id:
            raise HTTPException(status_code=400, detail="You can only read Log Data for your own Devices!")
        device_event = await crud.device_event.get_by_id(db, customer_device_id=customer_device_id, event_id=event_id)
    return device_event
