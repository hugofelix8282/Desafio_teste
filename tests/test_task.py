from http import HTTPStatus
import pytest

@pytest.mark.asyncio
def test_criar_tarefa(auth_client):
    payload = {"titulo": "Nova Tarefa", "descricao": "Descrição de teste"}
    response = auth_client.post("/task/", json=payload)
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["titulo"] == payload["titulo"]

@pytest.mark.asyncio
def test_listar_tarefas_usuario(auth_client):
    response = auth_client.get("/task/")
    assert response.status_code == HTTPStatus.CREATED
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
def test_obter_tarefa(auth_client):
    payload = {"titulo": "Buscar", "descricao": "Buscar tarefa"}
    response = auth_client.post("/task/", json=payload)
    tarefa_id = response.json()["id"]

    response = auth_client.get(f"/task/{tarefa_id}")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["id"] == tarefa_id

@pytest.mark.asyncio
def test_atualizar_tarefa(auth_client):
    payload = {"titulo": "Atualizar", "descricao": "Descrição"}
    response = auth_client.post("/task/", json=payload)
    tarefa_id = response.json()["id"]

    nova = {"titulo": "Atualizado", "descricao": "Nova descrição"}
    response = auth_client.put(f"/task/{tarefa_id}", json=nova)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["titulo"] == "Atualizado"

@pytest.mark.asyncio
def test_deletar_tarefa(auth_client):
    payload = {"titulo": "Para deletar", "descricao": "Descrição"}
    response = auth_client.post("/task/", json=payload)
    tarefa_id = response.json()["id"]

    response = auth_client.delete(f"/task/v1/{tarefa_id}")
    assert response.status_code == HTTPStatus.ACCEPTED

    response = auth_client.get(f"/task/{tarefa_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND

from http import HTTPStatus

@pytest.mark.asyncio
def test_criar_tarefa_titulo_vazio(auth_client):
    payload = {"titulo": "", "descricao": "Sem título válido"}
    response = auth_client.post("/task/", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

@pytest.mark.asyncio
def test_obter_tarefa_inexistente(auth_client):
    response = auth_client.get("/task/99999")  # ID presumivelmente inexistente
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_tarefa_inexistente(auth_client):
    payload = {"titulo": "Teste", "descricao": "Teste"}
    response = auth_client.put("/task/99999", json=payload)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_deletar_tarefa_inexistente(auth_client):
    response = auth_client.delete("/task/v1/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND

