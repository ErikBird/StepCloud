from sqlmodel import Field, SQLModel


class SensorTypeUpdate(SQLModel):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True)


class SensorTypeCreate(SQLModel):
    label: str = Field(index=True)


class SensorType(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True, sa_column_kwargs={"unique": True})
