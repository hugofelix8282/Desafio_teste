from db.session import create_database

def init():
    create_database()
    print(" Tabelas da Base de dados Criada com Sucesso!.")