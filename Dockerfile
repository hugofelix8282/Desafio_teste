# Dockerfile
FROM python:3.11-slim

# definindo um ambiente 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# criando um diretório app
WORKDIR /app

# instalando as dependências 
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

#copia do projeto
COPY . .

# Run app
CMD ["uvicorn", "Challenge_ProPig.main:app", "--host", "0.0.0.0", "--port", "8000"]
