# tests/conftest.py
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from Challenge_ProPig.db.base import Base
from Challenge_ProPig.main import app
from Challenge_ProPig.db.session import get_db
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        await asyncio.sleep(1)  # aguarda container inicializar
        yield postgres
        


@pytest_asyncio.fixture(scope="session")
async def session(postgres_container):
    engine = create_async_engine(postgres_container.get_connection_url().replace("postgresql://", "postgresql+asyncpg://"))
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as s:
        yield s

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_client(session):
    # Override get_db para usar sessão do Testcontainer
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
