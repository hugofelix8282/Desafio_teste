from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schema.v1 import tarefa as _schema
from service.v1 import task_service as _service
from db.session import get_db
from security.dependencies import get_current_user
from Models import models

router = APIRouter(prefix="/v1/task", tags=["Tarefas"])


 #Cria uma nova tarefa para o usuário autenticado.
@router.post("/", response_model=_schema.TarefaResponse, status_code=status.HTTP_201_CREATED)
async def criar_tarefa(
    tarefa_data: _schema.TarefaCreate,
    db: AsyncSession = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user),
):

    try:
        return await _service.criar_tarefa(tarefa_data, db, usuario.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Lista todas as tarefas do usuário autenticado.
@router.get("/", response_model=List[_schema.TarefaResponse])
async def listar_tarefas_usuario( db: AsyncSession = Depends(get_db),usuario: models.Usuario = Depends(get_current_user)):
    return await _service.listar_tarefas_usuario(db, usuario.id)

#Obtém uma tarefa específica do usuário autenticado.
@router.get("/{tarefa_id}", response_model=_schema.TarefaResponse)
async def obter_tarefa( tarefa_id: int,db: AsyncSession = Depends(get_db),usuario: models.Usuario = Depends(get_current_user)):  
    tarefa = await _service.obter_tarefa(tarefa_id, db, usuario.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


# Atualiza uma tarefa existente do usuário autenticado.
@router.put("/{tarefa_id}", response_model=_schema.TarefaResponse)
async def atualizar_tarefa(tarefa_id: int,tarefa_data: _schema.TarefaUpdate,db: AsyncSession = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)):
    tarefa = await _service.atualizar_tarefa(tarefa_id, tarefa_data, db, usuario.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Deleta uma tarefa existente do usuário autenticado.
@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa(
    tarefa_id: int,
    db: AsyncSession = Depends(get_db),
    usuario: models.Usuario = Depends(get_current_user)
):
    sucesso = await _service.deletar_tarefa(tarefa_id, db, usuario.id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa excluída com sucesso"}
