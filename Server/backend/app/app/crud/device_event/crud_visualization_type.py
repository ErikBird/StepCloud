from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base import CRUDBase
from app.sqlmodels.device_event.visualization_type import VisualizationType, VisualizationTypeCreate, \
    VisualizationTypeUpdate


class CRUDVisualizationType(CRUDBase[VisualizationType, VisualizationTypeCreate, VisualizationTypeUpdate]):
    async def get_by_label(self, db: AsyncSession, *, label: str) -> Optional[VisualizationType]:
        statement = select(VisualizationType).filter(VisualizationType.label == label)
        query = await db.exec(statement)
        return query.one_or_none()


visualization_type = CRUDVisualizationType(VisualizationType)
