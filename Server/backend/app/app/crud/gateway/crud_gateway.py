from app.crud.base import CRUDBase
from app.sqlmodels.gateway import Gateway, GatewayCreate, GatewayUpdate
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.crud.base import CRUDBase
from sqlalchemy.orm import selectinload
from app import sqlmodels, crud
from sqlmodel import select


class CRUDGateway(CRUDBase[Gateway, GatewayCreate, GatewayUpdate]):
    async def get(self, uuid: str, db: AsyncSession) -> Optional[Gateway]:
        statement = select(Gateway).where(Gateway.uuid == uuid).options(selectinload('*'))
        query = await db.exec(statement)
        return query.first()

    async def get_multi_by_customer(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100, customer_id: int) -> List[Gateway]:
        statement = select(Gateway).join(sqlmodels.CustomerOffice) \
            .where(sqlmodels.CustomerOffice.customer_id == customer_id).options(selectinload('*'))
        query = await db.exec(statement)
        return query.all()


gateway = CRUDGateway(Gateway)
