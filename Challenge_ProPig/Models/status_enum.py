from enum import Enum

# Class para habilitar o tipo de status a ser implementado.
class StatusEnum(str, Enum):
    pendente = "pendente"
    concluida = "concluida"
