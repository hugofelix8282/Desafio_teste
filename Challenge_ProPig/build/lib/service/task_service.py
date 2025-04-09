import fastapi as _fastapi
from schema import tarefa as _schema
from models import models
import datetime as _dt
import sqlalchemy.orm as _orm 

# servico para criação de tarefa 
def criar_tarefa(tarefa_data: _schema.TarefaCreate, db: Session, usuario_id: int):
    tarefa = models.Tarefa( titulo=tarefa_data.titulo, descricao=tarefa_data.descricao,usuario_id=usuario_id)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa

# Lista de tarefas do usuário 
def listar_tarefas_usuario(db: _orm.Session, usuario_id: int):
    return db.query(models.Tarefa).filter(models.Tarefa.usuario_id == usuario_id).all()

# obter tarefa especifica 
def obter_tarefa(tarefa_id: int, db: _orm.Session, usuario_id: int):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id, models.Tarefa.usuario_id == usuario_id).first()
    if not tarefa:
        raise _fastapi.HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

# atualização da tarefa 
def atualizar_tarefa(tarefa_id: int, tarefa_data: _schema.TarefaUpdate, db: _orm.Session, usuario_id: int):
    tarefa = obter_tarefa(tarefa_id, db, usuario_id)
    tarefa.titulo = tarefa_data.titulo
    tarefa.descricao = tarefa_data.descricao
    tarefa.status = tarefa_data.status
    if tarefa.status == "concluida":
        tarefa.data_conclusao = _dt.datetime.now(_dt.timezone.utc)
    db.commit()
    db.refresh(tarefa)
    return tarefa

def deletar_tarefa(tarefa_id: int, db: _orm.Session, usuario_id: int):
    tarefa = obter_tarefa(tarefa_id, db, usuario_id)
    db.delete(tarefa)
    db.commit()
