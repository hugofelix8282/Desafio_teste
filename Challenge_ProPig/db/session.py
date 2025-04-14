from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from db.base import Base
from config.settings import settings
from typing import AsyncIterator

#  Habilitar a conexão e comunicação com o database.
engine = create_async_engine(settings.database_url, echo=True)

# Criação de sessão async. 
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Cria todoas as tabela para o database.
async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Injeção de dependência  FastAPI
async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
