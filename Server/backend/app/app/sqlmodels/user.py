from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from sqlalchemy import UniqueConstraint
from pydantic import EmailStr
from .customer import Customer, CustomerReadWithOffice


# Shared properties
class UserBase(SQLModel):
    email: Optional[EmailStr]
    is_active: Optional[bool] = Field(default=True)
    is_superuser: Optional[bool] = Field(default=False)
    first_name: Optional[str]
    last_name: Optional[str]
    customer_id: Optional[int]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    customer_id: int


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str]


class UserRead(UserBase):
    hashed_password: str = Field(nullable=False)
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class UserWithCustomer(UserBase):
    hashed_password: str = Field(nullable=False)
    id: int
    customer: Optional["CustomerReadWithOffice"] = None
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class User(UserBase, table=True):
    __table_args__ = (UniqueConstraint("email"),)
    id: int = Field(primary_key=True, index=True)
    hashed_password: str = Field(nullable=False)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="users")
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
