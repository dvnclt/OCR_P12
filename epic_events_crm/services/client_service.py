import logging
from sqlalchemy.exc import SQLAlchemyError

from repositories.client_repository import ClientRepository
from auth_service import require_permission, is_contact


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    @require_permission("create_client")
    def create_client(self, user, full_name: str, email: str, phone: str,
                      company_name: str, contact: str):
        """
        Crée un nouveau client après vérification de l'email et de
        l'utilisateur contact.
        """
        try:
            if self.client_repo.get_client_by_email(email):
                logging.warning(f"Adresse email déjà existante : {email}")
                return {"error": "Cette adresse email est déjà utilisée"}, 400

            new_client = self.client_repo.create_client(
                full_name, email, phone, company_name, contact
            )
            return new_client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la création du client : "
                          f"{str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("read_client")
    def get_client_by_id(self, user, client_id: int):
        """Récupère un client par ID, renvoie une erreur si non trouvé."""
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.warning(f"Client ID {client_id} introuvable")
                return {"error": "Client introuvable"}, 404
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la récupération du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("read_client")
    def get_client_by_name(self, user, full_name: str):
        """
        Récupère un client par nom complet, renvoie une erreur si non trouvé.
        """
        try:
            client = self.client_repo.get_client_by_name(full_name)
            if not client:
                logging.warning(f"Client '{full_name}' introuvable")
                return {"error": "Client introuvable"}, 404
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la récupération du client "
                          f"{full_name}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("read_client")
    def get_client_by_email(self, user, email: str):
        """Récupère un client par email, renvoie une erreur si non trouvé."""
        try:
            client = self.client_repo.get_client_by_email(email)
            if not client:
                logging.warning(f"Client avec email {email} introuvable")
                return {"error": "Client introuvable"}, 404
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la récupération du client "
                          f"{email}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("update_client", object_check=is_contact)
    def update_client(self, user, client_id: int, full_name: str = None,
                      email: str = None, phone: str = None,
                      company_name: str = None, contact: str = None):
        """
        Met à jour les informations d'un client avec vérification de l'email.
        """
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.warning(f"Client ID {client_id} introuvable")
                return {"error": "Client introuvable"}, 404

            # Vérifier si l'email est déjà utilisé par un autre client
            if email and email != client.email:
                existing_client = self.client_repo.get_client_by_email(email)
                if existing_client and existing_client.id != client_id:
                    logging.warning(f"Adresse email déjà utilisée : {email}")
                    return {
                        "error": "Cette adresse email est déjà utilisée"
                        }, 400

            updated_client = self.client_repo.update_client(
                client_id, full_name, email, phone, company_name, contact
            )
            return updated_client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la mise à jour du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("delete_client")
    def delete_client(self, user, client_id: int):
        """Supprime un client par son ID avec vérification préalable."""
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.warning(f"Client ID {client_id} introuvable")
                return {"error": "Client introuvable"}, 404

            success = self.client_repo.delete_client(client_id)
            if success:
                return {"message": "Client supprimé avec succès"}, 200
            else:
                return {"error": "Erreur lors de la suppression"}, 500

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la suppression du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
