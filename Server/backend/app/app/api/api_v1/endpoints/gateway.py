from typing import Any, List
import logging
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, sqlmodels
from app.api import deps
from app.core import security

router = APIRouter()


@router.post("/create", response_model=sqlmodels.GatewayToken)
async def create_gateway(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        gateway_in: sqlmodels.GatewayCreate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Creates Gateway or returns existing Gateway
    """
    customer_office = await crud.customer_office.get(db=db, id=gateway_in.customer_office_id)
    if not customer_office:
        raise HTTPException(
            status_code=404,
            detail="The customer_office with this id does not exist in the system",
        )
    if not current_user.customer_id == customer_office.customer_id:
        raise HTTPException(
            status_code=400, detail="You can only create gateways for yourself."
        )
    gateway = await crud.gateway.get(db=db, uuid=gateway_in.uuid)
    if not gateway:
        gateway = await crud.gateway.create(db=db, obj_in=gateway_in)

    return sqlmodels.GatewayToken(access_token=security.create_access_token(gateway.uuid),
                                  refresh_token=security.create_refresh_token(gateway.uuid))


@router.get("/{uuid}/get-token", response_model=sqlmodels.GatewayToken)
async def create_gateway(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        uuid: str,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    gateway = await crud.gateway.get(db=db, uuid=uuid)
    if not gateway:
        raise HTTPException(
            status_code=404,
            detail="The gateway with this id does not exist in the system",
        )
    customer_office = await crud.customer_office.get(db=db, id=gateway.customer_office_id)
    if not current_user.customer_id == customer_office.customer_id:
        raise HTTPException(
            status_code=400, detail="You are not the gateway owner!"
        )

    return sqlmodels.GatewayToken(access_token=security.create_access_token(gateway.uuid),
                                  refresh_token=security.create_refresh_token(gateway.uuid))


@router.put("/update", response_model=sqlmodels.Gateway)
async def update_gateway(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        gateway_in: sqlmodels.GatewayUpdate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    gateway = await crud.gateway.get(db=db, uuid=gateway_in.uuid)
    if not gateway:
        raise HTTPException(
            status_code=404,
            detail="The gateway with this id does not exist in the system",
        )
    customer_office = await crud.customer_office.get(db=db, id=gateway.customer_office_id)
    if not current_user.customer_id == customer_office.customer_id:
        raise HTTPException(
            status_code=400, detail="You are not the gateway owner!"
        )
    user = await crud.gateway.update(db=db, db_obj=gateway, obj_in=gateway_in)
    return user


@router.get("/me", response_model=List[sqlmodels.Gateway])
async def get_gateways(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    gateways = await crud.gateway.get_multi_by_customer(db=db, skip=skip, limit=limit,
                                                        customer_id=current_user.customer_id)
    return gateways
