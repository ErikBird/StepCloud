from sqlalchemy import create_engine
from sqlalchemy import event
import time
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings


def get_async_db_uri() -> str:
    # set the below in your environment file when running tests
    if settings.TESTING:
        return settings.TEST_DATABASE_URI_ASYNC
    else:
        return settings.SQLALCHEMY_DATABASE_URI_ASYNC


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine_async = create_async_engine(get_async_db_uri(), pool_pre_ping=True)
async_session = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
