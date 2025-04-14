import pytest
from http import HTTPStatus

@pytest.mark.asyncio
async def test_criar_tarefa(auth_client_with_token):
    payload = {"titulo": "Nova Tarefa", "descricao": "Descrição de teste"}
    response = auth_client_with_token.post("/v1/task/", json=payload)  # Usando o cliente autenticado
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["titulo"] == payload["titulo"]

@pytest.mark.asyncio
async def test_listar_tarefas_usuario(auth_client_with_token):
    response = auth_client_with_token.get("/v1/task/")  # Usando o cliente autenticado
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_obter_tarefa(auth_client_with_token):
    payload = {"titulo": "Buscar", "descricao": "Buscar tarefa"}
    response = auth_client_with_token.post("/v1/task/", json=payload)  # Usando o cliente autenticado
    tarefa_id = response.json()["id"]

    response = auth_client_with_token.get(f"/v1/task/{tarefa_id}")  # Usando o cliente autenticado
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == tarefa_id

@pytest.mark.asyncio
async def test_atualizar_tarefa(auth_client_with_token):
    payload = {"titulo": "Atualizar", "descricao": "Descrição"}
    response = auth_client_with_token.post("/v1/task/", json=payload)  # Usando o cliente autenticado
    tarefa_id = response.json()["id"]

    nova = {"titulo": "Atualizado", "descricao": "Nova descrição"}
    response = auth_client_with_token.put(f"/v1/task/{tarefa_id}", json=nova)  # Usando o cliente autenticado
    assert response.status_code == HTTPStatus.OK
    assert response.json()["titulo"] == "Atualizado"

@pytest.mark.asyncio
async def test_deletar_tarefa(auth_client_with_token):
    payload = {"titulo": "Para deletar", "descricao": "Descrição"}
    response = auth_client_with_token.post("/v1/task/", json=payload)  # Usando o cliente autenticado
    tarefa_id = response.json()["id"]

    response = auth_client_with_token.delete(f"/v1/task/{tarefa_id}")  # Usando o cliente autenticado
    assert response.status_code == HTTPStatus.ACCEPTED

    response = auth_client_with_token.get(f"/v1/task/{tarefa_id}")  # Usando o cliente autenticado
    assert response.status_code == HTTPStatus.NOT_FOUND