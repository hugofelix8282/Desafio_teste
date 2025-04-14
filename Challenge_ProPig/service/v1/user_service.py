from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Models.models import Usuario
from schema.v1 import usuario as usuario_schema, token as token_schema
from passlib.context import CryptContext
from pydantic import EmailStr
from security.jwt_handler import criar_acesso_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def obter_usuario_email(email: str, db: AsyncSession):
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    return result.scalars().first()

async def criar_usuario(user: usuario_schema.UsuarioCreate, db: AsyncSession):
    # Validação de email é automaticamente feita pelo Pydantic se EmailStr for usado
    hashed_password = pwd_context.hash(user.password)
    novo_usuario = Usuario(email=user.email, nome=user.nome, hashed_password=hashed_password)
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario

async def autenticar_usuario(email: EmailStr, password: str, db: AsyncSession):
    usuario = await obter_usuario_email(email=email, db=db)
    if not usuario or not pwd_context.verify(password, usuario.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")
    token_jwt = criar_acesso_token(data={"sub": usuario.email})
    return token_schema.Token(access_token=token_jwt, token_type="Bearer")
