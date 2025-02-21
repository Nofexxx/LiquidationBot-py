import pytest_asyncio
import pytest
import asyncio

from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from unittest.mock import patch

import os
from sqlalchemy import create_engine, text

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="module")
def setup_db():
    postgres = PostgresContainer(
        "postgres:15-alpine",
        username="test",
        password="test",
        dbname="test"
    )
    postgres.start()

    os.environ["POSTGRES_HOST"] = postgres.get_container_host_ip()
    os.environ["POSTGRES_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["POSTGRES_USER"] = "test"
    os.environ["POSTGRES_PASS"] = "test"
    os.environ["POSTGRES_DB"] = "test"

    from scripts.db_config import Base
    sync_engine = create_engine(
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASS']}@"
        f"{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    )

    Base.metadata.create_all(sync_engine)
    yield

    Base.metadata.drop_all(sync_engine)
    postgres.stop()

@pytest_asyncio.fixture(scope="module")
async def setup_redis():
    redis = RedisContainer("redis:7-alpine")
    redis.start()

    os.environ["REDIS_HOST"] = redis.get_container_host_ip()
    os.environ["REDIS_PORT"] = str(redis.get_exposed_port(6379))

    from scripts.config import get_redis_client
    redis_client = get_redis_client()

    yield

    redis_client.close()
    redis.stop()