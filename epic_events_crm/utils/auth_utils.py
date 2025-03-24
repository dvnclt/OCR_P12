import os

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error, InvalidHashError


ph = PasswordHasher()

TOKEN_FILE = os.path.expanduser("~/.epic_events_token")


def set_token(token: str):
    """Stocke le token de manière persistante dans un fichier."""
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def get_token():
    """Récupère le token depuis le fichier, s'il existe."""
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()
    return token


def clear_token():
    """Supprime le token du fichier."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def set_password(password: str) -> str:
    # Hash le mot de passe avant de le stocker
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    # Vérifie si le mot de passe correspond au hash stocké
    try:
        return ph.verify(hashed_password, password)
    except (Argon2Error, InvalidHashError):
        return False
