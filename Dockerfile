# Base mais estável e com menos vulnerabilidades conhecidas
FROM python:3.11-slim-bullseye

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para build de pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências do Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia os arquivos do projeto
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para rodar o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
