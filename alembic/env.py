import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from sqlalchemy import pool

# Importa  base
from Challenge_ProPig.db.base import Base
from Challenge_ProPig.config.settings import settings

# Configurações do Alembic
config = context.config
fileConfig(config.config_file_name)

# Define a metadata
target_metadata = Base.metadata

DATABASE_URL = settings.database_url

# Função para executar as migrações
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # Compara tipos de colunas
        render_as_batch=True  # Necessário para SQLite em modo async, pode remover se for PostgreSQL
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)


    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

# Entry point
if context.is_offline_mode():
    do_run_migrations()
else:
    asyncio.run(run_migrations_online())