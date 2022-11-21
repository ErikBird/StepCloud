from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app.sqlmodels.device_event.log_type import LogType, LogTypeCreate, LogTypeUpdate


class CRUDLogType(CRUDBase[LogType, LogTypeCreate, LogTypeUpdate]):
    async def get_by_label(self, db: AsyncSession, *, label: str) -> Optional[LogType]:
        statement = select(LogType).where(LogType.label == label)
        query = await db.exec(statement)
        return query.one_or_none()


log_type = CRUDLogType(LogType)
