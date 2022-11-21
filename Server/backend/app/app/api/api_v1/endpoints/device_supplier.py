from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[sqlmodels.DeviceSupplier])
async def read_device_supplier(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    device_supplier = await crud.device_supplier.get_multi(db, skip=skip, limit=limit)
    return device_supplier
