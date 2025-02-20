import logging
from sqlalchemy.exc import SQLAlchemyError

from repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    def create_client(self, full_name: str, email: str, phone: str,
                      company_name: str, contact: str):
        """
        Crée un nouveau client après vérification de l'email et de
        l'utilisateur contact.
        """
        try:
            if self.client_repo.get_client_by_email(email):
                logging.debug(f"Adresse email déjà existante : {email}")
                return {"error": "Cette adresse email est déjà utilisée"}

            new_client = self.client_repo.create_client(
                full_name, email, phone, company_name, contact
            )
            return new_client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la création du client : "
                          f"{str(e)}")
            return {"error": "Erreur interne du serveur"}

    def get_client_by_id(self, client_id: int):
        """Récupère un client par ID, renvoie une erreur si non trouvé."""
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.debug(f"Client ID {client_id} introuvable")
                return {"error": "Client introuvable"}
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la récupération du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def get_client_by_email(self, email: str):
        """Récupère un client par email, renvoie une erreur si non trouvé."""
        try:
            client = self.client_repo.get_client_by_email(email)
            if not client:
                logging.debug(f"Client avec email {email} introuvable")
                return {"error": "Client introuvable"}
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la récupération du client "
                          f"{email}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def update_client(self, client_id: int, full_name: str = None,
                      email: str = None, phone: str = None,
                      company_name: str = None, contact: str = None):
        """
        Met à jour les informations d'un client avec vérification de l'email.
        """
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.debug(f"Client ID {client_id} introuvable")
                return {"error": "Client introuvable"}

            # Vérifier si l'email est déjà utilisé par un autre client
            if email and email != client.email:
                existing_client = self.client_repo.get_client_by_email(email)
                if existing_client and existing_client.id != client_id:
                    logging.debug(f"Adresse email déjà utilisée : {email}")
                    return {
                        "error": "Cette adresse email est déjà utilisée"
                        }

            updated_client = self.client_repo.update_client(
                client_id, full_name, email, phone, company_name, contact
            )
            return updated_client

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la mise à jour du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def delete_client(self, client_id: int):
        """Supprime un client par son ID avec vérification préalable."""
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.debug(f"Client ID {client_id} introuvable")
                return {"error": "Client introuvable"}

            success = self.client_repo.delete_client(client_id)
            if success:
                return {"message": "Client supprimé avec succès"}
            else:
                return {"error": "Erreur lors de la suppression"}

        except SQLAlchemyError as e:
            logging.error("Erreur SQL lors de la suppression du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}
