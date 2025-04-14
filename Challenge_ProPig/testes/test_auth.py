import pytest_asyncio
import jwt
from datetime import datetime, timedelta
from httpx import AsyncClient
from pathlib import Path
from Models.models import Usuario  # Ajuste conforme onde está seu modelo User

ALGORITHM = "RS256"
PRIVATE_KEY_PATH = Path(__file__).resolve().parent / "keys" / "fake_private.pem"
with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

def gerar_token(usuario_id: int):
    dados = {
        "sub": str(usuario_id),
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    return jwt.encode(dados, PRIVATE_KEY, algorithm=ALGORITHM)

# Supondo que você já tenha uma fixture `user` que cria um usuário teste
@pytest_asyncio.fixture(scope="function")
async def token(user: Usuario):
    return gerar_token(user.id)

# Usa a fixture `async_client` do conftest.py
@pytest_asyncio.fixture(scope="function")
async def auth_client(async_client: AsyncClient, token: str):
    async_client.headers.update({"Authorization": f"Bearer {token}"})
    return async_client
