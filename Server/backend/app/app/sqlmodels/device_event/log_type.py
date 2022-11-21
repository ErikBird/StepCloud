from sqlmodel import Field, SQLModel


class LogTypeUpdate(SQLModel):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True)


class LogTypeCreate(SQLModel):
    label: str = Field(index=True)


class LogType(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True, sa_column_kwargs={"unique": True})
