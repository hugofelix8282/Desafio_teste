import jwt
from Models import models
import sqlalchemy.orm as _orm
from schema import usuario as _user
from validador import validador_email
from security.securitty_password import Hasher
from security.jwt_handler import criar_acesso_token
import fastapi as _fastapi

# restaurar a usuário por email da base de dados.
def obter_usuário_email(email:str, db: _orm.Session):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

async def criar_usuario(user: _user.UsuarioCreate, db: _orm.Session):
    try:
       # validando o email
       valid_email = validador_email.valid_email(user.email)  

    except Exception:
         raise _fastapi.HTTPException(status_code=400, detail="Email formato invalido")  

    # hashing o password
    hashed_password=Hasher.obter_password_hash(user.password) 

    # criar instância do usuário
    user_obj = models.Usuario(email=valid_email, nome=user.nome, hashed_password=hashed_password)
    # adicionar usuário na base de dados
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


# autenticar o usuário para gerar o token.
async def autenticar_usuario(email:str, password:str, db: _orm.Session):

    user = await obter_usuário_email(email=email, db=db)
    if not user or not Hasher.verificar_password(password,user.hashed_password):
        raise _fastapi.HTTPException(status_code=401,detail="Email ou senha inválido")

    token= criar_acesso_token({"sub": user.email})
    return  _user.Token(access_token=token, token_type="bearer")





