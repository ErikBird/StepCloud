from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app.sqlmodels.device_event.event_type import EventType, EventTypeCreate, EventTypeUpdate


class CRUDEventType(CRUDBase[EventType, EventTypeCreate, EventTypeUpdate]):
    async def get_by_label(self, db: AsyncSession, *, label: str) -> Optional[EventType]:
        statement = select(EventType).where(EventType.label == label)
        query = await db.exec(statement)
        return query.one_or_none()


event_type = CRUDEventType(EventType)
