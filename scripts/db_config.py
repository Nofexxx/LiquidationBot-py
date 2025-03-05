# db_config.py

# Template for db_config.py

# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from contextlib import asynccontextmanager
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.asyncio import AsyncEngine
# from typing import AsyncGenerator


# Base = declarative_base()

# def get_connection_string() -> str:
#     host: str | None = os.environ.get('POSTGRES_HOST')
#     port: str | None = os.environ.get('POSTGRES_PORT')
#     user: str | None = os.environ.get('POSTGRES_USER')
#     password: str | None = os.environ.get('POSTGRES_PASS')
#     dbname: str | None = os.environ.get('POSTGRES_DB')

#     return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}'

# def get_engine() -> AsyncEngine:
#     return create_async_engine(
#         get_connection_string(),
#         pool_pre_ping=True,
#         pool_size=10,
#         max_overflow=20,
#         pool_timeout=60,
#     pool_recycle=600
# )



# @asynccontextmanager
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     async_session = async_sessionmaker(
#         get_engine(),
#         class_=AsyncSession,
#         expire_on_commit=False
#     )
#     session: AsyncSession = async_session()
#     try:
#         yield session
#     except:
#         await session.rollback()
#         raise
#     finally:
#         await session.close()
