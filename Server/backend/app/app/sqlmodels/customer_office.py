from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Session, SQLModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .customer import Customer
    from .customer_device import CustomerDevice
    from .gateway import Gateway


class CustomerOfficeBase(SQLModel):
    customer_id: Optional[int] = Field(foreign_key="customer.id")
    name: Optional[str]
    department: Optional[str]
    sub_department: Optional[str]
    zip_code: Optional[str]
    additional_address_information: Optional[str]
    street: Optional[str]
    city: Optional[str]
    country: Optional[str]


class CustomerOfficeCreate(CustomerOfficeBase):
    customer_id: int


class CustomerOfficeUpdate(CustomerOfficeBase):
    id: int
    customer_id: int


class CustomerOfficeRead(CustomerOfficeBase):
    id: int


class CustomerOffice(CustomerOfficeBase, table=True):
    id: int = Field(primary_key=True, index=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="offices")
    devices: List["CustomerDevice"] = Relationship(back_populates="office")
    gateways: List["Gateway"] = Relationship(back_populates="office")


from .customer_device import CustomerDeviceReadWithDevice


class CustomerOfficeReadWithCustomerDevices(CustomerOfficeBase):
    id: Optional[int]
    devices: List[CustomerDeviceReadWithDevice] = None
