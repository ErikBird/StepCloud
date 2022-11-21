from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlmodel import select, Session
from src import sqlmodels


class CRUDPostRequest:
    def delete_all(self, db: Session):
        statement = select(sqlmodels.PostRequest)
        query = db.exec(statement)
        for element in query.all():
            db.delete(element)
        db.commit()

    def get_all(self, db: Session) -> list[sqlmodels.PostRequest]:
        statement = select(sqlmodels.PostRequest)
        query = db.exec(statement)
        return query.all()

    def create(self, post_request_in: sqlmodels.PostRequestCreate, db: Session) -> Optional[sqlmodels.PostRequest]:
        obj_in_data = jsonable_encoder(post_request_in)
        post_request_db = sqlmodels.PostRequest(**obj_in_data)
        db.add(post_request_db)
        db.commit()
        db.refresh(post_request_db)
        return post_request_db


post_request = CRUDPostRequest()
