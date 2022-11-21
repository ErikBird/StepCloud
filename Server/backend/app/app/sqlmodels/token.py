from typing import Optional
from sqlmodel import SQLModel
import datetime


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: Optional[int] = None


class GatewayTokenPayload(SQLModel):
    sub: Optional[str] = None
    exp: datetime.datetime


class GatewayToken(SQLModel):
    access_token: str
    refresh_token: str


class AccessToken(SQLModel):
    access_token: str
