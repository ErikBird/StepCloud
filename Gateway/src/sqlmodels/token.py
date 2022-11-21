from typing import Optional
from sqlmodel import Field, SQLModel


class AccessToken(SQLModel):
    access_token: str


class RefreshToken(SQLModel):
    access_token: str


class AuthTokensCreate(SQLModel):
    access_token: str
    refresh_token: str


class AuthTokens(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    access_token: str
    refresh_token: str
