import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Models import models
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from security.jwt_handler import verificar_token
from db.session import get_db
from fastapi import Depends


# Configure logging
logger = logging.getLogger(__name__)

# OAuth2 Password Bearer token schema for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

# Dependency function to get the current user from the token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> models.Usuario:
    payload = verificar_token(token)
    email = payload.sub

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: email não encontrado"
        )

    stmt = select(models.Usuario).where(models.Usuario.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return user