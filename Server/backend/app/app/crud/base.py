from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import selectinload
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import Depends

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, id: Any, db: AsyncSession) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id).options(selectinload('*'))
        query = await db.exec(statement)
        return query.first()

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit).options(selectinload('*'))
        query = await db.exec(statement)
        return query.all()

    async def create(self, *, obj_in: CreateSchemaType, db: AsyncSession) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            db: AsyncSession,
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, *, id: int, db: AsyncSession) -> ModelType:
        obj = db.query(self.model).get(id)
        await db.delete(obj)
        await db.commit()
        return obj
