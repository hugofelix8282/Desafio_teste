from passlib.hash import bcrypt


class Hasher:
    '''
     Obter o password do usuário e criptografa através da lib bcrypy. 
                                                                      '''

    @staticmethod
    def obter_password_hash(password: str) -> str:
        return bcrypt.hash(password)
    

    @staticmethod
    def verificar_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    