from fastapi import FastAPI
from api.v1 import task_router, user_router
from contextlib import asynccontextmanager
from db.session import engine
from fastapi.middleware.cors import CORSMiddleware
import logging
from db.init_db import init 


# Subindo a aplicação e o database.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # === Startup ===
    logging.info(" Inicializando a aplicação e criando as tabelas...")
    await init()

    yield  
    logging.info(" Encerrando a aplicação...")

    try:
        await engine.dispose() 
        logging.info("Conexões com o banco foram encerradas.")

    except Exception as e:
        logging.warning(" Erro durante encerramento: %s", e)

app = FastAPI(
    title="Challenge ProPig",
    description="API para gerenciamento de tarefas com autenticação JWT",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina domínios específicos!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Buscando as Rotas dos serviços 
app.include_router(user_router.router)
app.include_router(task_router.router)

#  Rota raiz 
@app.get("/")
def read_root():
    return {"msg": "API de Tarefas com JWT está rodando!"}
