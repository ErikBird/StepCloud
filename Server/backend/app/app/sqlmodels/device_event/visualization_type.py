from sqlmodel import Field, SQLModel


class VisualizationTypeUpdate(SQLModel):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True)


class VisualizationTypeCreate(SQLModel):
    label: str = Field(index=True)


class VisualizationType(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    label: str = Field(index=True, sa_column_kwargs={"unique": True})
