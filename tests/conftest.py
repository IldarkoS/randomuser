import asyncio
import os

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.db import Base
from app.depends import get_async_session, get_users_random_api
from app.main import app
from tests.mocks import RandomUserApiMock

os.environ["ENV_FILE"] = ".env.test"
pytest_plugins = ["pytest_asyncio"]

from app.config import Settings
settings = Settings()
TEST_DATABASE_URL = settings.DATABASE_DSN
print(TEST_DATABASE_URL)
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestSession = sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    async def run():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(run())


@pytest.fixture(autouse=True)
def override_get_session():
    async def override():
        async with TestSession() as session:
            yield session
    app.dependency_overrides[get_async_session] = override


@pytest.fixture(autouse=True)
def override_random_user_api():
    def override():
        return RandomUserApiMock()
    app.dependency_overrides[get_users_random_api] = override
