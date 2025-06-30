import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_connection_string() -> str:
    host: str | None = os.environ.get("POSTGRES_HOST")
    port: str | None = os.environ.get("POSTGRES_PORT")
    user: str | None = os.environ.get("POSTGRES_USER")
    password: str | None = os.environ.get("POSTGRES_PASS")
    dbname: str | None = os.environ.get("POSTGRES_DB")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"


def get_engine() -> AsyncEngine:
    return create_async_engine(
        get_connection_string(),
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=2,
        pool_timeout=60,
        pool_recycle=600,
    )


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        get_engine(), class_=AsyncSession, expire_on_commit=False
    )
    session: AsyncSession = async_session()
    try:
        yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
