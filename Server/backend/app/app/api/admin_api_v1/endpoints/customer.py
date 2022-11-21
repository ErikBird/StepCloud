from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.post("/", response_model=sqlmodels.Customer, summary="Create a new Customer")
async def create_customer(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        customer_in: sqlmodels.CustomerCreate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new customer.
    """
    customer = await crud.customer.get_by_name(db=db, name=customer_in.name)
    if customer:
        raise HTTPException(
            status_code=400,
            detail="A customer with this name already exists in the system.",
        )
    customer = await crud.customer.create(db=db, obj_in=customer_in)
    return customer


@router.get("/", response_model=List[sqlmodels.Customer])
async def read_customer(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve customer.
    """
    if await crud.user.is_superuser(current_user):
        customers = await crud.customer.get_multi(db=db, skip=skip, limit=limit)
    else:
        customers = [await crud.customer.get(db=db, id=current_user.customer_id)]
    return customers
