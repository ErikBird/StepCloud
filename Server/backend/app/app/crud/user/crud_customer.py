from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app.sqlmodels.customer import Customer, CustomerCreate, CustomerUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Customer]:
        statement = select(Customer).filter(Customer.name == name)
        query = await db.exec(statement)
        return query.one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: CustomerCreate) -> Customer:
        db_obj = Customer(
            name=obj_in.name,
            vat_id=obj_in.vat_id,
            contract_level=obj_in.contract_level
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Customer]:
        statement = select(self.model).offset(skip).limit(limit)
        query = await db.exec(statement)
        return query.all()


customer = CRUDCustomer(Customer)
