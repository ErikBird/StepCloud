from typing import List, Optional
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, col

from app.crud.base import CRUDBase
from app.sqlmodels.identifier import Identifier, IdentifierCreate, IdentifierUpdate, IdentifierReadWithDevices
from sqlalchemy.orm import selectinload


class CRUDIdentifier(CRUDBase[Identifier, IdentifierCreate, IdentifierUpdate]):
    async def get_by_expression(self, db: AsyncSession, *, expression: str) -> Optional[IdentifierReadWithDevices]:
        statement = select(Identifier).where(Identifier.expression == expression).options(
            selectinload(Identifier.device)
        )
        query = await db.exec(statement)
        return query.one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: IdentifierCreate) -> Identifier:
        db_identifier = Identifier.from_orm(obj_in)
        db.add(db_identifier)
        await db.commit()
        await db.refresh(db_identifier)
        return db_identifier

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Identifier]:
        statement = select(self.model).offset(skip).limit(limit)
        query = await db.exec(statement)
        return query.all()


identifier = CRUDIdentifier(Identifier)
