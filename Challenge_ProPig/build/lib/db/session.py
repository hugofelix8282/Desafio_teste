from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from config.settings import settings

# Criar o mecanismo com base na URL vinda do settings
engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# criar todas as tabelas 
def create_database():
    Base.metadata.create_all(bind=engine)

# Injeção de dependência para o FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
