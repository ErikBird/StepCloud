from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, Session
from fastapi import Depends
from src import sqlmodels
import uuid


class CRUDUUID:
    def get(self, db: Session) -> Optional[sqlmodels.UUID]:
        statement = select(sqlmodels.UUID)
        query = db.exec(statement)
        return query.first()

    def create(self, db: Session) -> Optional[sqlmodels.UUID]:
        uuid_generated = str(uuid.uuid4())
        db_obj = sqlmodels.UUID(value=uuid_generated)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_or_create(self, db: Session):
        my_uuid = self.get(db=db)

        if not my_uuid:
            my_uuid = self.create(db=db)

        return my_uuid

    """
    def update(self, db: Session, uuid_update: str) -> Optional[sqlmodels.UUID]:
        statement = select(sqlmodels.UUID)
        query = db.exec(statement)
        db_uuid = query.first()
        db_uuid.value = uuid_update
        db.add(db_uuid)
        db.commit()
        db.refresh(db_uuid)
        return db_uuid
    """


uuid_gateway = CRUDUUID()
