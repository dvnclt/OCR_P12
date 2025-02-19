import functools
import logging
import os

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error, InvalidHashError

from utils.jwt_utils import get_current_user

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


def check_permission(user, permission_name: str):
    """
    Vérifie si l'utilisateur a une permission spécifique.
    """
    if not user or not user.role or not user.role.permissions:
        return False  # Aucune permission disponible
    user_permissions = {perm.name for perm in user.role.permissions}
    return permission_name in user_permissions


def require_permission(permission):
    """
    Décorateur pour vérifier une permission
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Récupération de l'utilisateur à partir du contexte
            token = get_token()
            if not token:
                raise Exception("Authentification requise")
            user = get_current_user(token, self.user_repo)
            if not user:
                logging.warning("Utilisateur non authentifié")
                return {"error": "Utilisateur non authentifié"}, 401

            # Vérifier la permission globale
            if not check_permission(user, permission):
                logging.warning("Permission refusée pour {user.email} : "
                                f"{permission}")
                return {"error": "Permission refusée"}, 403

            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def is_contact(user, client=None, contract=None, event=None):
    """
    Vérifie si l'utilisateur est le contact assigné
    """
    if client.user_id == user.id:
        return True
    if contract.user_id == user.id:
        return True
    if event:
        if event.user_id == user.id:
            return True
        if event.contract:
            contract = event.contract
            if contract.user_id == user.id and contract.contract_status == "Signé":  # noqa: E501
                return True
    return False
