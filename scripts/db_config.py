#db_config.py

#Template for db_config.py

# from dotenv import load_dotenv
# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from contextlib import asynccontextmanager
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# def get_connection_string():
#     host = os.environ.get('POSTGRES_HOST')
#     port = os.environ.get('POSTGRES_PORT')
#     user = os.environ.get('POSTGRES_USER')
#     password = os.environ.get('POSTGRES_PASS')
#     dbname = os.environ.get('POSTGRES_DB')
    
#     return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}'

# def get_engine():
#     return create_async_engine(
#         get_connection_string(),
#         pool_pre_ping=True,
#         pool_size=10,
#         max_overflow=20,
#         pool_timeout=60,
#     pool_recycle=600
# )



# @asynccontextmanager
# async def get_db_session():
#     async_session = sessionmaker(
#     get_engine(), 
#     class_=AsyncSession, 
#     expire_on_commit=False
# )
#     session = async_session()
#     try:
#         yield session
#     except:
#         await session.rollback()
#         raise
#     finally:
#         await session.close()