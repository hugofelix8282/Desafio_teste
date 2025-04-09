import pytest
import pytest_asyncio
from httpx import AsyncClient
from datetime import datetime, timedelta
import jwt
from Challenge_ProPig.schema import tarefa as tarefa_schema
from Challenge_ProPig.Models import models


ALGORITHM = "RS256"
with open("keys/fake_private.pem", "rb") as f:
    PRIVATE_KEY = f.read()


def gerar_token(usuario_id: int):
    dados = {
        "sub": str(usuario_id),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    return jwt.encode(dados, PRIVATE_KEY, algorithm=ALGORITHM)

@pytest_asyncio.fixture(scope="function")
async def token(user):
    return gerar_token(user.id)


@pytest_asyncio.fixture(scope="function")
async def auth_client(client: AsyncClient, token: str):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client