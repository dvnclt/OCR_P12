import logging
from sqlalchemy.exc import SQLAlchemyError
from repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    def create_client(self, full_name: str, email: str, phone: str,
                      company_name: str, contact: str):
        """
        Crée un nouveau client dans la base de données.
        Vérifie que l'email du client n'existe pas déjà.
        """
        try:
            existing_client = self.client_repo.get_client_by_email(email)
            if existing_client:
                logging.warning(f"Adresse email déjà existante : {email}")
                return {"error": "Cet adresse email est déjà utilisée"}, 400

            new_client = self.client_repo.create_client(
                full_name, email, phone, company_name, contact
            )
            return new_client

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la création du client : {str(e)}")
            return {"error": "Erreur interne"}, 500

    def get_client_by_id(self, client_id: int):
        """
        Récupère un client par son ID.
        Retourne une erreur si le client n'existe pas.
        """
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.warning("Client introuvable")
                return {"error": "Client introuvable"}, 404
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération du client "
                          f"{client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def get_client_by_name(self, full_name: str):
        """
        Récupère un client par son nom complet.
        Retourne une erreur si le client n'existe pas.
        """
        try:
            client = self.client_repo.get_client_by_name(full_name)
            if not client:
                logging.warning(f"Client introuvable : {full_name}")
                return {"error": "Client introuvable"}, 404
            return client

        except Exception as e:
            logging.error("Erreur lors de la récupération du client avec le "
                          f"nom {full_name}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def get_client_by_email(self, email: str):
        """
        Récupère un client par son email.
        Retourne une erreur si le client n'existe pas.
        """
        try:
            client = self.client_repo.get_client_by_email(email)
            if not client:
                logging.warning(f"Client introuvable depuis : {email}")
                return {"error": "Client introuvable"}, 404
            return client

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération du client depuis "
                          f"{email}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def update_client(self, client_id: int, full_name: str = None,
                      email: str = None, phone: str = None,
                      company_name: str = None, contact: str = None):
        """
        Met à jour les informations d'un client.
        Modifie son nom, email, téléphone, entreprise ou contact.
        """
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.warning("Client introuvable")
                return {"error": "Client introuvable"}, 404

            updated_client = self.client_repo.update_client(
                client_id, full_name, email, phone, company_name, contact
            )
            return updated_client

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la mise à jour : {str(e)}")
            return {"error": "Erreur interne"}, 500

    def delete_client(self, client_id: int):
        """Supprime un client par son ID."""
        try:
            client = self.client_repo.get_client_by_id(client_id)
            if not client:
                logging.warning("Client introuvable")
                return {"error": "Client introuvable"}, 404

            success = self.client_repo.delete_client(client_id)
            if success:
                return {"message": "Client supprimé"}, 200
            else:
                return {"error": "Erreur lors de la suppression"}, 500

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la suppression : {str(e)}")
            return {"error": "Erreur interne"}, 500
