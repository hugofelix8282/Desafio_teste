from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException, status

# check a validade do email.
def valid_email(email: str) -> str:
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email invalido.")
