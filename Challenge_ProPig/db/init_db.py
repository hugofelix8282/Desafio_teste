from db.session import create_database

async def init():
    await create_database()
    print(" Tabelas da Base de dados Criada com Sucesso!.")