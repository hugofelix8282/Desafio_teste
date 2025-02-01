import pika
import schemas as _schemas
import service as _services
import fastapi as _fastapi
import sqlalchemy.orm as _orm

class User_Client(object):
        
    async def create_user(
        user: _schemas.UserCreate, 
        db: _orm.Session = _fastapi.Depends(_services.get_db)):
        db_user = await _services.get_user_by_email(email=user.email, db=db)
        
        if db_user:
            raise _fastapi.HTTPException(
                status_code=400,
                detail="User with that email already exists")

        user = await _services.create_user(user=user, db=db)

        return _fastapi.HTTPException(
                status_code=201,
                detail="User Registered, Please verify email to activate account !")

                
