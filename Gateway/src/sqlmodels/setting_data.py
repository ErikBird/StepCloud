from sqlmodel import Field, SQLModel, Column, JSON


# Shared properties
class SettingData(SQLModel):
    # Label which describe the Content of the Event to the user
    label: str = Field(index=True)
    # Payload -> all Settings Data converted into a JSON compatible format
    data: dict = Field(sa_column=Column(JSON))

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True
