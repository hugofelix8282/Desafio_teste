#  Validador de Titulo não vázio.
def validar_titulo_nao_vazio( value: str) -> None:
    if not value.strip():      
        raise ValueError("O título não pode estar vazio ou apenas com espaços.")
    return value