import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from db.session import Base
from sqlalchemy import Enum as SqlEnum
from enums.status_enum import StatusEnum
from typing import Optional, List
from sqlalchemy import String, Text, DateTime 
from sqlalchemy.orm import Mapped, mapped_column, relationship,registry
import datetime as dt

table_registry = registry()

@table_registry.mapped_as_dataclass
class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    tarefas: Mapped[List["Tarefa"]] = relationship("Tarefa", back_populates="usuario")

    def verificar_password(self, password: str) -> bool:
        
       # Verifica se a senha fornecida confere com a senha criptografada.
    
        return _hash.bcrypt.verify(password, self.hashed_password)

@table_registry.mapped_as_dataclass
class Tarefa(Base):
    __tablename__ = "tarefa"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    data_criacao: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc),
        nullable=False
    )

    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.pendente)

    data_conclusao: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="tarefas")
     # Função habilitada para definir a hora e data de cluclusão da tarefa, quando o usúario a definir como concluída.
    def update_status(self, new_status: StatusEnum) -> None:
        self.status = new_status
        if new_status == StatusEnum.concluida:
            self.data_conclusao = dt.datetime.now(dt.timezone.utc)
        else:
            self.data_conclusao = None
    
