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

from src.constants.const import System


class CRUDToken:
    def get(self, db: Session) -> Optional[sqlmodels.AuthTokens]:
        statement = select(sqlmodels.AuthTokens)
        query = db.exec(statement)
        return query.first()

    def create(self, tokens: sqlmodels.AuthTokensCreate, db: Session) -> Optional[sqlmodels.AuthTokens]:
        db_obj = sqlmodels.AuthTokens(access_token=tokens.access_token,
                                      refresh_token=tokens.refresh_token)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, access_token: str, db: Session):
        token = self.get(db=db)
        token.access_token = access_token
        db.add(token)
        db.commit()
        db.refresh(token)
        System.AUTH_TOKEN = token


token = CRUDToken()
