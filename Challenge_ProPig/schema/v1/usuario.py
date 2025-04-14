
from pydantic import BaseModel, ConfigDict, EmailStr,Field
from typing import Optional

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
         model_config = ConfigDict(from_attributes=True)



