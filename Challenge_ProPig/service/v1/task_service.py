from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schema.v1 import tarefa as schema
from Models import models, status_enum

# Serviço para criação de tarefa
async def criar_tarefa(tarefa_data: schema.TarefaCreate, db: AsyncSession, usuario_id: int):
    tarefa = models.Tarefa(
        titulo=tarefa_data.titulo,
        descricao=tarefa_data.descricao,
        usuario_id=usuario_id
    )
    db.add(tarefa)
    await db.commit()
    await db.refresh(tarefa)
    return tarefa

# Lista de tarefas do usuário
async def listar_tarefas_usuario(db: AsyncSession, usuario_id: int):
    result = await db.execute(
        select(models.Tarefa).where(models.Tarefa.usuario_id == usuario_id)
    )
    return result.scalars().all()

# obter tarefas do usuário especifica.
async def obter_tarefa(tarefa_id: int, db: AsyncSession, usuario_id: int):
    stmt = select(models.Tarefa).where(
        models.Tarefa.id == tarefa_id,
        models.Tarefa.usuario_id == usuario_id
    )
    result = await db.execute(stmt)
    tarefa = result.scalar_one_or_none()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# Atualização da tarefa
async def atualizar_tarefa(tarefa_id: int, tarefa_data: schema.TarefaUpdate, db: AsyncSession, usuario_id: int):
    tarefa = await obter_tarefa(tarefa_id, db, usuario_id)
    tarefa.titulo = tarefa_data.titulo
    tarefa.status = tarefa_data.status
    if tarefa.status == status_enum.StatusEnum.concluida:
        tarefa.data_conclusao = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(tarefa)
    return tarefa

# Deletar tarefa
async def deletar_tarefa(tarefa_id: int, db: AsyncSession, usuario_id: int) -> bool:
    tarefa = await obter_tarefa(tarefa_id, db, usuario_id)
    if tarefa:
        await db.delete(tarefa)
        await db.commit()
        return True
    return False