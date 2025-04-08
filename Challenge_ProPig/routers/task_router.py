import fastapi as _fastapi
from sqlalchemy.orm import _orm
from typing import List
from schema import tarefa as _schema
from services import tarefa_service as _service
from db.session import get_db
from auth.dependencies import get_current_user
from models import models

router = APIRouter(prefix="/task", tags=["Tarefas"])

@router.post("/", response_model=_schema.TarefaResponse, status_code=_fastapi.status.HTTP_201_CREATED)
def criar_tarefa(tarefa_data: _schema.TarefaCreate,db: _orm.Session = _fastapi.Depends(get_db),
usuario: models.Usuario = _fastapi.Depends(get_current_user),):
    return _service.criar_tarefa(tarefa_data, db, usuario.id)


@router.get("/", response_model=List[_schema.TarefaResponse])
def listar_tarefas_usuario(
    db: _orm.Session = _fastapi.Depends(get_db),
    usuario: models.Usuario = _fastapi.Depends(get_current_user),):
    return _service.listar_tarefas_usuario(db, usuario.id)


@router.get("/{tarefa_id}", response_model=_schema.TarefaResponse)
def obter_tarefa(
    tarefa_id: int,
    db: _orm.Session = _fastapi.Depends(get_db),
    usuario: models.Usuario = _fastapi.Depends(get_current_user),
):
    return _service.obter_tarefa(tarefa_id, db, usuario.id)


@router.put("/{tarefa_id}", response_model=_schema.TarefaResponse)
def atualizar_tarefa(
    tarefa_id: int,
    tarefa_data: _schema.TarefaUpdate,
    db: _orm.Session = _fastapi.Depends(get_db),
    usuario: models.Usuario = _fastapi.Depends(get_current_user),
):
    return _service.atualizar_tarefa(tarefa_id, tarefa_data, db, usuario.id)


@router.delete("/v1/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(
    tarefa_id: int,
    db: _orm.Session = _fastapi.Depends(get_db),
    usuario: models.Usuario = _fastapi.Depends(get_current_user),
):
    _service.deletar_tarefa(tarefa_id, db, usuario.id)
    return None
