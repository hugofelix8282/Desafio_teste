import fastapi as _fastapi
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from schema.v1 import usuario as _user
from service.v1 import user_service as _service
from db.session import get_db  

router = _fastapi.APIRouter(prefix="/v1/auth", tags=["auth"])

# Criar registro de usuario
@router.post("/registro", response_model=_user.UsuarioResponse)
async def registro(user: _user.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    return await _service.criar_usuario(user, db)

# Realizar Login do Usuário
@router.post("/login")
async def login( form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await _service.autenticar_usuario(form_data.username, form_data.password, db)
