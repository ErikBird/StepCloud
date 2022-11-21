from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, col
from app.crud.base import CRUDBase
from app.sqlmodels.device import Device, DeviceCreate, DeviceUpdate, DeviceReadWithRelationships
from app.sqlmodels.identifier import Identifier, IdentifierCreate
from sqlalchemy.orm import selectinload, lazyload


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[DeviceReadWithRelationships]:
        statement = select(Device).filter(Device.name == name)
        query = await db.exec(statement)
        return query.one_or_none()

    async def get_by_identifier(self, db: AsyncSession, expression: str) -> Optional[DeviceReadWithRelationships]:
        identifier = await db.get(Identifier, expression)
        if not identifier:
            return None
        statement = select(Device).where(Device.id == identifier.device_id).options(selectinload('*'))
        # .options(selectinload(Device.identifiers))
        query = await db.exec(statement)
        result = query.one()
        return result

    async def create_with_identifiers(self, db: AsyncSession, *, obj_in: DeviceCreate) -> Device:
        db_device = Device(
            name=obj_in.name,
            supplier_id=obj_in.supplier_id
        )
        for expression in obj_in.identifiers:
            Identifier(expression=expression, device=db_device)
        db.add(db_device)
        await db.commit()
        await db.refresh(db_device)
        return db_device

    async def get_multi_with_identifier(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[DeviceReadWithRelationships]:
        statement = select(self.model).offset(skip).limit(limit).options(selectinload('*'))
        query = await db.exec(statement)
        return query.all()


device = CRUDDevice(Device)
