from typing import Optional
from sqlmodel import Field, SQLModel


class Config(SQLModel):
    uuid: str = ''
    serial_number: str = ''
    software_version: str
    hardware_version: str
    authenticated: bool
    network_address: str
