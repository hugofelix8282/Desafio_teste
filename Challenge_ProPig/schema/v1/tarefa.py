from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import Optional
from datetime import datetime
from Models.status_enum import  StatusEnum
from validators.tarefa_valid_tittle import validar_titulo_nao_vazio    


class TarefaBase(BaseModel):
    titulo: str = Field(..., max_length=255)
    descricao: Optional[str] = Field(default=None, max_length=500)
    _validar_titulo = field_validator("titulo")(validar_titulo_nao_vazio)  # validar título caso vázio

class TarefaCreate(TarefaBase):
    pass

class TarefaUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, max_length=255)
    status: Optional[StatusEnum]
    _validar_titulo = field_validator("titulo")(validar_titulo_nao_vazio)  # validar título caso vázio

class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: StatusEnum
    data_criacao: datetime
    data_conclusao: Optional[datetime]

    class Config:
        model_config = ConfigDict(from_attributes=True)

class TarefaDeleteResponse(BaseModel):
    detail: str = Field(..., response="Tarefa deletada com sucesso.")
