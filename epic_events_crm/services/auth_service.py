import functools
import logging

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


def check_permission(user, permission_name: str):
    """
    Vérifie si l'utilisateur a une permission spécifique.
    """
    if not user or not user.role or not user.role.permissions:
        return False  # Aucune permission disponible
    user_permissions = {perm.name for perm in user.role.permissions}
    return permission_name in user_permissions


def require_permission(permission, object_check=None):
    """
    Décorateur pour vérifier une permission + une condition sur un objet.

    :param permission: Nom de la permission requise.
    :param object_check: Fonction qui prend (user, obj) et retourne True/False.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, user, obj_id, *args, **kwargs):
            # Récupération de l'objet client
            obj = self.client_repo.get_client_by_id(obj_id)
            if not obj:
                logging.warning(f"Client ID {obj_id} introuvable")
                return {"error": "Client introuvable"}, 404

            # Vérifier la permission globale
            if not check_permission(user, permission):
                # Vérifier une condition spécifique
                if object_check and not object_check(user, obj):
                    logging.warning(f"Permission refusée pour {user.email}: "
                                    "Tentative de modification du client "
                                    f"{obj_id}")
                    return {"error": "Permission refusée"}, 403

            return func(self, user, obj, *args, **kwargs)
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
