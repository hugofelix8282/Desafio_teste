# Desafio Teste Prático 
## instruções do projeto 

### Realizar os testes
Instruçõees para realizar os testes através do bibioteca python-pytest. 
> a biblioteca testcontainers-python foi atribuída  para subir um banco de dados PostgreSQL isolado para os testes. logo, temos uma separação do  container postgres de desenvolvimento, do container testes. 

* No terminal raiz do seu projeto (conftest.py), rode:
```
pytest
```

* Obter  detalhes dos testes:
```
pytest -v
```
ver detalhes com print() incluído:
```
pytest -s
```  

### Docker 
Instruções para subir a aplicação via docker compose. 
> observe que Para usar o Docker Compose, você precisa tê-lo instalado em seu sistema. Ele não está incluído na instalação padrão do Docker, então lembre-se de instalá-lo separadamente!

* No terminal, na raiz do projeto, execute:
```
docker-compose up --build  
```
* Para rodar em background:
```
docker-compose up -d --build
```
* Acesse sua aplicação no navegador:
```
http://localhost:8000/docs

```







