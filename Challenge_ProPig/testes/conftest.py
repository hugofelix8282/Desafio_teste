import asyncio
import pytest
import pytest_asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from main import app
from db.session import get_db
from fastapi.testclient import TestClient
import time
from sqlalchemy import text 
import jwt
from datetime import datetime, timedelta

DATABASE_URL = "postgresql+asyncpg://testuser:testpass@localhost:5433/testdb"

# Criação global do engine e sessionmaker para reaproveitamento
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Fixture do loop de eventos
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# Fixture para o banco de dados com escopo de sessão
@pytest_asyncio.fixture(scope="session")
async def session():
    # Aguarda o banco subir
    for _ in range(10):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            break
        except Exception:
            print("Aguardando banco de dados iniciar...")
            await asyncio.sleep(2)
    else:
        raise RuntimeError("Não foi possível conectar ao banco de dados de teste.")

    # Cria as tabelas antes dos testes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        async with async_session() as s:
            yield s  # sessão usada durante os testes
    finally:
        print("Limpando banco de dados de teste...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


# Fixture do cliente autenticado com injeção de dependência
@pytest_asyncio.fixture(scope="session")
async def auth_client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client


# Fixture para criação de token JWT para testes
@pytest_asyncio.fixture(scope="function")
async def token(user):
    ALGORITHM = "RS256"
    with open("keys/fake_private.pem", "rb") as f:
        PRIVATE_KEY = f.read()

    def gerar_token(usuario_id: int):
        payload = {
            "sub": str(usuario_id),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
        return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

    return gerar_token(user.id)


# Cliente autenticado com o token JWT nos headers
@pytest_asyncio.fixture(scope="function")
async def auth_client_with_token(auth_client, token):
    auth_client.headers.update({"Authorization": f"Bearer {token}"})
    return auth_client