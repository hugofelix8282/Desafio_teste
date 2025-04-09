from fastapi import Depends, HTTPException, status
import fastapi as _fastapi
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
import sqlalchemy.orm as _orm
from  security.jwt_handler import verificar_token
from db.session import get_db
from Models import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/login")

def get_current_user(token: str = _fastapi.Depends(oauth2_scheme), db: _orm.Session = _fastapi.Depends(get_db)
):
    try:
        # Decodificar e verificar o token
        payload = verificar_token(token)
        user_id: int = payload.get("id")

        if user_id is None:
            raise HTTPException(
                status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        # Obter o usuário da base de dados.
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

        if user is None:
            raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        return user

    except _fastapi.HTTPException:
        raise
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_401_UNAUTHORIZED, detail=str(e))
