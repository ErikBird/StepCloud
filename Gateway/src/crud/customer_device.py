from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlmodel import select, Session
from src import sqlmodels


class CRUDCustomerDevice:
    def get_all(self, db: Session) -> list[sqlmodels.CustomerDevice]:
        statement = select(sqlmodels.CustomerDevice)
        query = db.exec(statement)
        return query.all()

    def create(self, customer_device: sqlmodels.CustomerDevice, db: Session) -> Optional[sqlmodels.CustomerDevice]:
        db.add(customer_device)
        db.commit()
        db.refresh(customer_device)
        return customer_device


customer_device = CRUDCustomerDevice()
