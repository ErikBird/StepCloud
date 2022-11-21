from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.put("/", response_model=sqlmodels.CustomerOffice)
async def update_customer_office(
        customer_office_in: sqlmodels.CustomerOfficeUpdate,
        db: AsyncSession = Depends(deps.async_get_db),
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update Customer Office.
    """

    customer_office_obj = await crud.customer_office.get(db=db, id=customer_office_in.id)
    if not customer_office_obj:
        raise HTTPException(
            status_code=404, detail="The customer office does not exist"
        )
    logging.error(customer_office_in.customer_id)
    logging.error(customer_office_obj.customer_id)
    if customer_office_in.customer_id != customer_office_obj.customer_id:
        raise HTTPException(
            status_code=400, detail="Customer Id is not correct!"
        )
    if customer_office_in.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=400, detail="You can only edit your own customer office!"
        )
    customer_office = await crud.customer_office.update(db=db, db_obj=customer_office_obj,
                                                        obj_in=customer_office_in)
    return customer_office
