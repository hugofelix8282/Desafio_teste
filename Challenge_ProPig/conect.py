import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text 

DATABASE_URL = "postgresql+asyncpg://testuser:testpass@localhost:5433/testdb"

async def testar_conexao():
    try:
        engine = create_async_engine(DATABASE_URL, echo=False)
        async with engine.begin() as conn:
             await conn.execute(text("SELECT 1")) 
        print("✅ Conexão com o banco de dados bem-sucedida.")
    except Exception as e:
        print("❌ Erro ao conectar ao banco de dados:")
        print(str(e))

if __name__ == "__main__":
    asyncio.run(testar_conexao())