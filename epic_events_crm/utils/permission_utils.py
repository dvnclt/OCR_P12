import functools
import logging

from utils.jwt_utils import get_current_user
from utils.auth_utils import get_token


def check_permission(user, permission_name: str):
    """
    Vérifie si l'utilisateur a une permission spécifique.
    """
    if not user or not user.role or not user.role.permissions:
        return False  # Aucune permission disponible
    user_permissions = {perm.name for perm in user.role.permissions}
    return permission_name in user_permissions


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
            if contract.user_id == user.id:
                return True
    return False


def require_permission(permission, check_ownership=False):
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
                logging.debug("Utilisateur non authentifié")
                return {"error": "Utilisateur non authentifié"}

            # Vérifier la permission globale
            if not check_permission(user, permission):
                logging.debug("Permission refusée pour {user.email} : "
                              f"{permission}")
                return {"error": "Permission refusée"}

            # Vérifier si l'utilisateur est responsable
            if check_ownership:
                event = kwargs.get("event", None)
                contract = kwargs.get("contract", None)
                client = kwargs.get("client", None)
                if not is_contact(user, client, contract, event):
                    logging.debug(f"Accès refusé pour {user.email}, "
                                  "non responsable.")
                    return {"error": "Accès refusé : vous n'êtes pas "
                            "responsable"}
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
