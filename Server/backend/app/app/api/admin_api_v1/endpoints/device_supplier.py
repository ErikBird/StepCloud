from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.post("/", response_model=sqlmodels.DeviceSupplier)
async def create_device_supplier(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        device_supplier_in: sqlmodels.DeviceSupplierBase,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    device_supplier = await crud.device_supplier.get_by_name(db, name=device_supplier_in.name)
    if device_supplier:
        raise HTTPException(
            status_code=400,
            detail="A Device Supplier with this name already exists in the system.",
        )
    device_supplier = await crud.device_supplier.create(db, obj_in=device_supplier_in)
    return device_supplier
