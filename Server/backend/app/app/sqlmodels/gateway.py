from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from .customer_office import CustomerOffice


# Shared properties
class GatewayBase(SQLModel):
    uuid: Optional[str]  # Automatic ID generated on the client
    customer_office_id: Optional[int] = Field(foreign_key="customeroffice.id")
    serial_number: Optional[str]
    software_version: Optional[str]
    hardware_version: Optional[str]


class GatewayCreate(GatewayBase):
    uuid: str
    customer_office_id: int


class GatewayUpdate(GatewayBase):
    uuid: str


class GatewayRead(GatewayBase):
    uuid: str


class Gateway(GatewayBase, table=True):
    uuid: str = Field(primary_key=True, index=True)
    customer_office_id: int = Field(foreign_key="customeroffice.id")
    office: "CustomerOffice" = Relationship(back_populates="gateways")


from .customer_office import CustomerOfficeReadWithCustomerDevices


class GatewayReadWithOffice(GatewayBase):
    uuid: str
    office: "CustomerOfficeReadWithCustomerDevices" = None
