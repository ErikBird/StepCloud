from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud
from app.crud.base import CRUDBase
from app import sqlmodels
from sqlmodel import select


class CRUDLogData(CRUDBase[sqlmodels.LogData, sqlmodels.LogDataCreate, sqlmodels.LogDataUpdate]):
    async def get_by_event_id(self, db: AsyncSession, *, device_event_id: int):
        statement = select(self.model).where(sqlmodels.LogData.event_id == device_event_id)
        query = await db.exec(statement)
        return query.all()

    async def create(self, db: AsyncSession, *, obj_in: sqlmodels.LogDataCreate) \
            -> sqlmodels.LogData:
        log_type = await crud.log_type.get_by_label(db=db, label=obj_in.log_type)
        db_obj = sqlmodels.LogData(label=obj_in.label,
                                   data=obj_in.data,
                                   event_id=obj_in.event_id,
                                   log_type_id=log_type.id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


log_data = CRUDLogData(sqlmodels.LogData)
