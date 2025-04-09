from fastapi import FastAPI
from routers import task_router, user_router
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import logging
from db.init_db import init 


@asynccontextmanager
async def lifespan(app: FastAPI):
    # === Startup ===
    logging.info("🚀 Inicializando a aplicação e criando as tabelas...")
    init()

    yield  
    # === Shutdown ===
    logging.info("🛑 Encerrando a aplicação... (Você pode fechar conexões ou liberar recursos aqui)")

app = FastAPI(
    title="Challenge ProPig",
    description="API para gerenciamento de tarefas com autenticação JWT",
    version="1.0.0",
    lifespan=lifespan
)

# === Logging Config ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina domínios específicos!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Rotas ===
app.include_router(user_router.router)
app.include_router(task_router.router)

# === Rota raiz ===
@app.get("/")
def read_root():
    return {"msg": "API de Tarefas com JWT está rodando!"}
