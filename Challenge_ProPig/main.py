from fastapi import FastAPI
from routers import task_router, user_router

app = FastAPI(
    title="Challenge ProPig",
    description="API para gerenciamento de tarefas com autenticação JWT",
    version="1.0.0"
)


# === Logging Config ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # alterar em produção!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Routers 
app.include_router(user_router.router)
app.include_router(task_router.router)

# Root route
@app.get("/")
def read_root():
    return {"msg": "API de Tarefas com JWT está rodando!"}
