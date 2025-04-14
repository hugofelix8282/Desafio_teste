import pytest
from http import HTTPStatus


# criar usuário
@pytest.mark.asyncio
async def test_criar_usuario_sucesso(async_client):
    response = async_client.post("/v1/auth/registro", json={
        "nome": "João Valido",
        "email": "joaovalido@example.com",
        "password": "senha123"
    })
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["email"] == "joaovalido@example.com"
    assert "id" in data


# Test creating user with invalid email
@pytest.mark.asyncio
async def test_criar_usuario_email_invalido(async_client):
    response = async_client.post("/v1/auth/registro", json={
        "nome": "João",
        "email": "email-invalido",
        "password": "senha123"
    })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Test creating user with short password
@pytest.mark.asyncio
async def test_criar_usuario_senha_curta(async_client):
    response = async_client.post("/v1/auth/registro", json={
        "nome": "João",
        "email": "joaoteste@example.com",
        "password": "12"
    })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Test login with valid credentials
@pytest.mark.asyncio
async def test_login_usuario_sucesso(async_client):
    # Registro antes do login
    await async_client.post("/auth/v1/registro", json={
        "nome": "Maria",
        "email": "maria@example.com",
        "password": "senhateste"
    })

    response = await async_client.post("/auth/v1/login", data={
        "username": "maria@example.com",
        "password": "senhateste"
    })
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# Test login with wrong password
@pytest.mark.asyncio
async def test_login_senha_errada(async_client):
    response = await async_client.post("/auth/v1/login", data={
        "username": "maria@example.com",
        "password": "senhaerrada"
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED


# Test login with non-existent email
@pytest.mark.asyncio
async def test_login_usuario_nao_existe(async_client):
    response = await async_client.post("/auth/v1/login", data={
        "username": "naoexiste@example.com",
        "password": "qualquersenha"
    })
    assert response.status_code == HTTPStatus.UNAUTHORIZED
