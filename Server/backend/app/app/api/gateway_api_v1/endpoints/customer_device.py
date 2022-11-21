from typing import Any, List
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, sqlmodels
from app.api import deps
import logging
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, sqlmodels

router = APIRouter()


@router.post("/create", response_model=sqlmodels.CustomerDevice)
async def create_customer_device_by_device_name(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        customer_device_in: sqlmodels.CustomerDeviceCreateByDeviceName,
        current_gateway: sqlmodels.Gateway = Depends(deps.get_current_gateway),
) -> Any:
    logging.error(customer_device_in.gateway_id)
    customerdevice = await crud.customer_device.get_by_customer_office_and_gateway_id(db=db,
                                                                                      customer_office_id=current_gateway.customer_office_id,
                                                                                      gateway_id=customer_device_in.gateway_id)
    logging.error(customerdevice)
    if customerdevice:
        return customerdevice
    device = await crud.device.get_by_identifier(db=db, expression=customer_device_in.device_type)
    if not device:
        raise HTTPException(status_code=400, detail="No Device in the system matches the given device_name")

    # Exchange the device_name with the device_id in the system
    obj_in_data = jsonable_encoder(customer_device_in)
    del obj_in_data['device_type']
    obj_in_data['device_id'] = device.id
    obj_in_data['customer_office_id'] = current_gateway.customer_office_id

    obj_in = sqlmodels.CustomerDeviceCreate(**obj_in_data)
    customerdevice_created = await crud.customer_device.create(db=db, obj_in=obj_in)
    return customerdevice_created


@router.get("/all", response_model=list[sqlmodels.CustomerDeviceReadWithDevice])
async def get_all_customer_devices_in_current_office(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        current_gateway: sqlmodels.Gateway = Depends(deps.get_current_gateway),
) -> Any:
    this_customer_office_id = current_gateway.customer_office_id
    customer_devices = await crud.customer_device.get_multi_by_customer_office(db=db,
                                                                               customer_office_id=this_customer_office_id)

    return customer_devices
