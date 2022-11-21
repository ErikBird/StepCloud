from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .customer_office import CustomerOffice
    from .customer_device import CustomerDevice


# Shared properties
class CustomerBase(SQLModel):
    name: Optional[str] = Field(index=True)
    vat_id: Optional[str] = Field(index=True)


# Properties to receive on item creation
class CustomerCreate(CustomerBase):
    name: str
    contract_level: int = 1


# Properties to receive on item update
class CustomerUpdate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    contract_level: int = Field(default=1, nullable=False)


class Customer(CustomerBase, table=True):
    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    contract_level: int = Field(default=1, nullable=False)
    users: List["User"] = Relationship(back_populates="customer")
    offices: List["CustomerOffice"] = Relationship(back_populates="customer")


from .customer_office import CustomerOfficeRead


class CustomerReadWithOffice(CustomerRead):
    id: int = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    contract_level: int = Field(default=1, nullable=False)
    offices: Optional[List[CustomerOfficeRead]] = []
