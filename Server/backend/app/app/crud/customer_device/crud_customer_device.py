from typing import Any, Dict, Optional, Union, List

from app import sqlmodels
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.sqlmodels.customer_device import CustomerDevice, CustomerDeviceCreate, CustomerDeviceUpdate, \
    CustomerDeviceReadWithDevice
from app.sqlmodels.customer import Customer
from sqlalchemy.orm import selectinload


class CRUDDeviceCustomer(CRUDBase[CustomerDevice, CustomerDeviceCreate, CustomerDeviceUpdate]):
    async def create_with_customer(
            self, db: AsyncSession, *, obj_in: CustomerDeviceCreate, db_obj: Customer) -> CustomerDevice:
        db_obj = CustomerDevice(
            device_id=obj_in.device_id,
            customer_id=db_obj.id,
            gateway_name=obj_in.gateway_name,
            network_ip=obj_in.network_ip,
            registration_code=obj_in.registration_code,
            serial_number=obj_in.serial_number,
            label=obj_in.label,
            customer_office_id=obj_in.customer_office_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[CustomerDevice]:
        statement = select(CustomerDevice).filter(CustomerDevice.id == id)
        query = await db.exec(statement)
        return query.one_or_none()

    async def get_by_customer_office_and_gateway_id(
            self, db: AsyncSession, *, customer_office_id: int, gateway_id: str) -> CustomerDeviceReadWithDevice:
        statement = select(CustomerDevice) \
            .where(CustomerDevice.customer_office_id == customer_office_id) \
            .where(CustomerDevice.gateway_id == gateway_id)
        query = await db.exec(statement)
        return query.one_or_none()

    async def get_multi_by_customer_office(
            self, db: AsyncSession, *, customer_office_id: int, skip: int = 0, limit: int = 100
    ) -> List[CustomerDeviceReadWithDevice]:
        statement = select(self.model).filter(self.model.customer_office_id == customer_office_id).offset(skip).limit(
            limit) \
            .options(selectinload('*'))
        query = await db.exec(statement)
        return query.all()

    async def get_multi_by_customer(
            self, db: AsyncSession, *, customer_id: int, skip: int = 0, limit: int = 100
    ) -> List[CustomerDeviceReadWithDevice]:
        statement = select(CustomerDevice).join(sqlmodels.CustomerOffice).filter(
            sqlmodels.CustomerOffice.customer_id == customer_id).offset(skip).limit(limit) \
            .options(selectinload('*'))
        # .options(selectinload(DeviceCustomer.device.identifier))
        query = await db.exec(statement)
        return query.all()

    async def update(
            self, db: AsyncSession, *, db_obj: CustomerDevice, obj_in: Union[CustomerDevice, Dict[str, Any]]
    ) -> CustomerDevice:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


customer_device = CRUDDeviceCustomer(CustomerDevice)
