from functools import lru_cache
from config.settings import settings


# carregar a chave privada 
@lru_cache()  # assegurar que a chave seja carrega apenas uma vez em disco. (@lru_cache)
def obter_chave_privada() -> bytes:
    with open(settings.JWT_PRIVATE_KEY_PATH, "rb") as f: 
        return f.read()

# carregar a chave privada 
@lru_cache()
def obter_chave_publica() -> bytes:
    with open(settings.JWT_PUBLIC_KEY_PATH, "rb") as f: 
        return f.read()
    
