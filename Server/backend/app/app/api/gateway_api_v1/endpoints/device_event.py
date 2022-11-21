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


@router.post("/create", response_model=sqlmodels.DeviceEvent)
async def create_device_event(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        device_event_in: sqlmodels.DeviceEventCreate,
        current_gateway: sqlmodels.Gateway = Depends(deps.get_current_gateway),
) -> Any:
    customerdevice = await crud.customer_device.get_by_id(db=db, id=device_event_in.customer_device_id)
    logging.error(customerdevice.id)
    if not customerdevice:
        raise HTTPException(status_code=404, detail="Customer-Device not found")
    if not current_gateway.customer_office_id == customerdevice.customer_office_id:
        raise HTTPException(status_code=403, detail="Wrong Office/Gateway Combination for your Customer-Device")

    sensor_event = await crud.device_event.create(db=db, obj_in=device_event_in)
    return sensor_event
