from app.crud.base import CRUDBase
from app.sqlmodels.customer_office import CustomerOffice, CustomerOfficeCreate, CustomerOfficeUpdate
from typing import Any, Dict, Optional, Union, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.sqlmodels.customer_device import CustomerDevice, CustomerDeviceCreate, CustomerDeviceUpdate, \
    CustomerDeviceReadWithDevice
from app.sqlmodels.customer import Customer
from sqlalchemy.orm import selectinload


class CRUDCustomerOffice(CRUDBase[CustomerOffice, CustomerOfficeCreate, CustomerOfficeUpdate]):
    async def get_by_customer_id(self, db: AsyncSession, *, customer_id: int) -> Optional[CustomerOffice]:
        statement = select(CustomerOffice).filter(CustomerOffice.customer_id == customer_id)
        query = await db.exec(statement)
        return query.all()


customer_office = CRUDCustomerOffice(CustomerOffice)
