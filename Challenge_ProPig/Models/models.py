import datetime as dt
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SqlEnum
from db.session import Base
from Models.status_enum import StatusEnum
import passlib.hash as _hash


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    tarefas: Mapped[List["Tarefa"]] = relationship(
        "Tarefa",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def verificar_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)

    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email}>"


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

    def update_status(self, new_status: StatusEnum) -> None:
        self.status = new_status
        if new_status == StatusEnum.concluida:
            self.data_conclusao = dt.datetime.now(dt.timezone.utc)
        else:
            self.data_conclusao = None

    def __repr__(self):
        return f"<Tarefa id={self.id} titulo={self.titulo} status={self.status}>"
