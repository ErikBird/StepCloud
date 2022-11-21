from typing import Optional

from sqlmodel import SQLModel, Field


class PostRequestCreate(SQLModel):
    target: str
    data: str


class PostRequest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    target: str
    data: str
