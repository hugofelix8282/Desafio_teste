from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from enums.status_enum import StatusEnum 

class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O título não pode estar vazio.")
        return value

class TarefaCreate(TarefaBase):
    pass  

class TarefaUpdate(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    status: Optional[StatusEnum]

class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: StatusEnum
    data_criacao: datetime
    data_conclusao: Optional[datetime]

    class Config:
        model_config = ConfigDict(from_attributes=True)
