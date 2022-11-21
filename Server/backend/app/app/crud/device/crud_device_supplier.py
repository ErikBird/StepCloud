from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.crud.base import CRUDBase
from app.sqlmodels.device_supplier import DeviceSupplier, DeviceSupplierCreate, DeviceSupplierUpdate
from sqlmodel import select


class CRUDDeviceSupplier(CRUDBase[DeviceSupplier, DeviceSupplierCreate, DeviceSupplierUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[DeviceSupplier]:
        statement = select(DeviceSupplier).filter(DeviceSupplier.name == name)
        query = await db.exec(statement)
        return query.one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: DeviceSupplierCreate) -> DeviceSupplier:
        db_obj = DeviceSupplier(
            name=obj_in.name,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[DeviceSupplier]:
        statement = select(self.model).offset(skip).limit(limit)
        query = await db.exec(statement)
        return query.all()


device_supplier = CRUDDeviceSupplier(DeviceSupplier)
