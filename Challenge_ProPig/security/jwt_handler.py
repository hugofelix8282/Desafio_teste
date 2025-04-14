import jwt
from typing import Union
import datetime as _dt
import  fastapi as  _fastapi
from security.jwt_keys import obter_chave_privada, obter_chave_publica
from schema.v1.token import TokenPayload 
from Models import models
from config.settings import settings

#  pegar as chaves publicas e privadas.
PRIVATE_KEY = obter_chave_privada()
PUBLIC_KEY = obter_chave_publica()


# Gerador de token (realizar codificação dos dados.)
def criar_acesso_token(data: dict, expires_delta: _dt.timedelta = None):
    to_encode = data.copy()
    expire = _dt.datetime.now(_dt.timezone.utc) + (expires_delta or _dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    endecode_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return endecode_jwt 



# Verificador de token (decodifica e valida a assinatura do JWT)
def verificar_token(token: str) -> Union[TokenPayload, None]:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        return TokenPayload.model_validate(payload)  
    except jwt.ExpiredSignatureError:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )    
    
    