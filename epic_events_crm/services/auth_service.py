from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error, InvalidHashError

ph = PasswordHasher()


def set_password(password: str) -> str:
    # Hash le mot de passe avant de le stocker
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    # Vérifie si le mot de passe correspond au hash stocké
    try:
        return ph.verify(hashed_password, password)
    except (Argon2Error, InvalidHashError):
        return False
