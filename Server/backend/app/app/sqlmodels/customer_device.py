from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .customer_office import CustomerOffice


# Shared properties
class CustomerDeviceBase(SQLModel):
    network_ip: Optional[str]
    registration_code: Optional[str]
    serial_number: Optional[str]


# Properties to receive on item creation
class CustomerDeviceCreate(CustomerDeviceBase):
    device_id: int
    gateway_id: str
    interface_name: str
    label: Optional[str]
    customer_office_id: Optional[int]


class CustomerDeviceCreateByDeviceName(CustomerDeviceBase):
    device_type: str
    gateway_id: Optional[str]
    label: Optional[str]
    interface_name: str


# Properties to receive on item update
class CustomerDeviceUpdate(CustomerDeviceBase):
    gateway_name: Optional[str]
    label: Optional[str]


class CustomerDeviceRead(CustomerDeviceBase):
    id: int = Field(primary_key=True, index=True)
    gateway_id: str = Field(nullable=False)
    interface_name: str
    device_id: int = Field(foreign_key="device.id")
    customer_office_id: int = Field(foreign_key="customeroffice.id")
    label: Optional[str]


class CustomerDevice(CustomerDeviceBase, table=True):
    id: int = Field(primary_key=True, index=True)
    gateway_id: str = Field(nullable=False)
    device_id: int = Field(foreign_key="device.id")
    customer_office_id: int = Field(foreign_key="customeroffice.id")
    office: "CustomerOffice" = Relationship(back_populates="devices")
    label: str
    interface_name: str
    device: "Device" = Relationship()


from .device import DeviceReadWithSupplier


class CustomerDeviceReadWithDevice(CustomerDeviceRead):
    device: Optional[DeviceReadWithSupplier] = None
