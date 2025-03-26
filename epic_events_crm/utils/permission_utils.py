import functools
import logging

from utils.jwt_utils import get_current_user
from utils.auth_utils import get_token
from repositories.client_repository import Client
from repositories.contract_repository import Contract
from repositories.event_repository import Event


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
    if client:
        if client.user_id == user.id:
            return True
    if contract:
        if contract.user_id == user.id:
            return True
    if event:
        if event.user_id == user.id:
            return True
        if event.contract:
            contract = event.contract
            if contract.user_id == user.id:
                return True
    print(client)
    print(contract)
    print(event)
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
                contract_id = kwargs.get("contract_id") or (
                    args[1] if len(args) > 1 else None)
                event_id = kwargs.get("event_id") or (
                    args[2] if len(args) > 2 else None)
                client_id = kwargs.get("client_id") or (
                    args[3] if len(args) > 3 else None)

                contract = self.event_repo.db.query(Contract).filter(
                    Contract.id == contract_id
                ).first() if contract_id else None

                event = self.event_repo.db.query(Event).filter(
                    Event.id == event_id
                ).first() if event_id else None

                client = self.event_repo.db.query(Client).filter(
                    Client.id == client_id
                ).first() if client_id else None

                if not is_contact(user, client=client, contract=contract,
                                  event=event):
                    logging.debug(f"Accès refusé pour {user.email}, non "
                                  "responsable.")
                    return {"error": "Accès refusé : vous n'êtes pas "
                            "responsable"}
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
