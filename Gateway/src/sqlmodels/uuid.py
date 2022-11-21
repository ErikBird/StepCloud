from sqlmodel import SQLModel, Field


class UUID(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    value: str
