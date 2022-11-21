from sqlmodel import Field, SQLModel


class EventTypeUpdate(SQLModel):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True)


class EventTypeCreate(SQLModel):
    label: str = Field(index=True)


class EventType(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True, sa_column_kwargs={"unique": True})
