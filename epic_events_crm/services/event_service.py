import logging
from sqlalchemy.exc import SQLAlchemyError

from repositories.event_repository import EventRepository
from models.client import Client
from models.contract import Contract
from models.user import User


class EventService:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def create_event(self, name: str, contract_id: int, client_id: int,
                     start_date: str, end_date: str, location: str,
                     attendees: int, contact: str, user_id: int, notes: str):
        """
        Crée un nouvel événement dans la base de données.
        Vérifie que le client, le contrat, et l'utilisateur existent
        """
        try:
            contract = self.event_repo.db.query(Contract).filter(
                Contract.id == contract_id
                ).first()
            if not contract:
                logging.debug(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}

            client = self.event_repo.db.query(Client).filter(
                Client.id == client_id
                ).first()
            if not client:
                logging.debug(f"Client introuvable : {client_id}")
                return {"error": "Client introuvable"}

            contact_user = self.event_repo.db.query(User).filter(
                User.id == user_id
                ).first()
            if not contact_user:
                logging.debug(f"Utilisateur introuvable : {user_id}")
                return {"error": "Utilisateur introuvable"}

            new_event = self.event_repo.create_event(
                name, contract_id, client_id, start_date, end_date, location,
                attendees, contact, user_id, notes
            )
            return new_event

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la création de l'événement : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}

    def get_event_by_id(self, event_id: int):
        """
        Récupère un événement par son ID.
        Retourne une erreur si l'événement n'existe pas.
        """
        try:
            event = self.event_repo.get_event_by_id(event_id)
            if not event:
                logging.debug(f"Événement introuvable : {event_id}")
                return {"error": "Événement introuvable"}
            return event

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération de l'événement "
                          f"{event_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def get_events_by_contract(self, contract_id: int):
        """
        Récupère tous les événements associés à un contrat donné.
        Retourne une erreur si aucun événement n'est trouvé.
        """
        try:
            events = self.event_repo.get_events_by_contract_id(contract_id)
            if not events:
                logging.debug("Aucun événement trouvé pour le contrat "
                              f"{contract_id}")
                return {"error": "Aucun événement trouvé"}
            return events

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération des événements du "
                          f"contrat {contract_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def get_events_by_client(self, client_id: int):
        """
        Récupère tous les événements associés à un client donné.
        Retourne une erreur si aucun événement n'est trouvé.
        """
        try:
            events = self.event_repo.get_events_by_client_id(client_id)
            if not events:
                logging.debug("Aucun événement trouvé pour le client "
                              f"{client_id}")
                return {"error": "Aucun événement trouvé"}
            return events

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération des événements du "
                          f"client {client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def get_events_by_user(self, user_id: int):
        """
        Récupère tous les événements associés à un utilisateur donné.
        Retourne une erreur si aucun événement n'est trouvé.
        """
        try:
            events = self.event_repo.get_events_by_user_id(user_id)
            if not events:
                logging.debug("Aucun événement trouvé pour l'utilisateur "
                              f"{user_id}")
                return {"error": "Aucun événement trouvé"}
            return events

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération des événements de "
                          f"l'utilisateur {user_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def update_event(self, event_id: int, name: str = None,
                     contract_id: int = None, client_id: int = None,
                     start_date: str = None, end_date: str = None,
                     location: str = None, attendees: int = None,
                     contact: str = None, user_id: int = None,
                     notes: str = None):
        """
        Met à jour les informations d'un événement.
        Modifie son nom, son contrat, son client, ses dates, son lieu, etc.
        """
        try:
            event = self.event_repo.get_event_by_id(event_id)
            if not event:
                logging.debug(f"Événement introuvable : {event_id}")
                return {"error": "Événement introuvable"}

            updated_event = self.event_repo.update_event(
                event_id, name, contract_id, client_id, start_date, end_date,
                location, attendees, contact, user_id, notes
            )
            return updated_event

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la mise à jour de l'événement "
                          f"{event_id}: {str(e)}")
            return {"error": "Erreur interne"}

    def delete_event(self, event_id: int):
        """
        Supprime un événement par son ID.
        Retourne une erreur si l'événement n'existe pas.
        """
        try:
            event = self.event_repo.get_event_by_id(event_id)
            if not event:
                logging.debug(f"Événement introuvable : {event_id}")
                return {"error": "Événement introuvable"}

            success = self.event_repo.delete_event(event_id)
            if success:
                return {"message": "Événement supprimé"}
            else:
                return {"error": "Erreur lors de la suppression"}

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la suppression de l'événement "
                          f"{event_id}: {str(e)}")
            return {"error": "Erreur interne"}
