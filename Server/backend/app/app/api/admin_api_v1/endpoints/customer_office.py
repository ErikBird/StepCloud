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


@router.get("/", response_model=List[sqlmodels.CustomerOfficeReadWithCustomerDevices])
async def read_customer_office(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    customer_office = await crud.customer_office.get_multi(db=db, skip=skip, limit=limit)
    if not customer_office:
        raise HTTPException(
            status_code=404,
            detail="No customer office in the system",
        )
    return customer_office


@router.post("/", response_model=sqlmodels.CustomerOffice)
async def create_customer_office(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        customer_office_in: sqlmodels.CustomerOfficeCreate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new customer office.
    """
    customer_office = await crud.customer_office.create(db=db, obj_in=customer_office_in)
    return customer_office
