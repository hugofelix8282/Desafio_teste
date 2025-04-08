import fastapi as _fastapi
import sqlalchemy.orm as _orm
from schema import usuario as _user
from service.user_service as _service
from db.session import get_db

router = _fastapi.APIRouter(prefix="/auth", tags["auth"])

# router endpoint registro
@router.post("/v1/registro",response_model=UsuarioResponse)
async def registro(user: _user.UsuarioCreate, db: _orm.Session = _fastapi.Depends(get_db)):
    return await _service.criar_usuario(user, db)

#router endpoint registro
@router.post("/v1/login")
async def login(user: _user.UsuarioLogin, db: Session = Depends(get_db)):
    return await _service.autenticar_usuario(user.email, user.password, db)


