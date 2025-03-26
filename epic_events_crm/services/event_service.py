import logging
import uuid
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from repositories.event_repository import EventRepository
from models.client import Client
from models.contract import Contract
from models.user import User
from utils.permission_utils import require_permission


class EventService:
    def __init__(self, event_repo: EventRepository, user_repo=None):
        self.event_repo = event_repo
        self.user_repo = user_repo

    @require_permission("create_event", check_ownership=True)
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

    @require_permission("read_event", check_ownership=False)
    def get_events(self, event_id: int = None,
                   contract_id: str = None,
                   client_id: str = None,
                   user_id: int = None,
                   start_date: datetime = None,
                   end_date: datetime = None,
                   no_user: bool = False
                   ):
        """
        Récupère les events selon les critères fournis
        Retourne une erreur si aucun event n'est trouvé.
        """
        try:
            if contract_id is not None:
                try:
                    uuid_obj = uuid.UUID(contract_id)  # noqa: F841
                except ValueError:
                    return {"error": "ID du contrat invalide"}
            events = self.event_repo.get_events(event_id=event_id,  # noqa: E501
                                                contract_id=contract_id,
                                                client_id=client_id,
                                                user_id=user_id,
                                                start_date=start_date,
                                                end_date=end_date,
                                                no_user=no_user
                                                )
            if not events:
                logging.debug("Aucun évènement trouvé pour les critères : "
                              f"event_id={event_id}",
                              f"contract_id={contract_id}",
                              f"client_id={client_id}",
                              f"user_id={user_id}",
                              f"start_date={start_date}",
                              f"end_date={end_date}",
                              f"no_user={no_user}",
                              )
                return {"error": "Aucun évènement trouvé"}

            return events

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des évènements : "
                          f"{str(e)}")
            return {"error": "Erreur interne du serveur"}

    @require_permission("update_event", check_ownership=True)
    def update_event(self, event_id: int, name: str = None,
                     start_date: str = None, end_date: str = None,
                     contact: str = None, location: str = None,
                     attendees: int = None, user_id: int = None,
                     notes: str = None):
        """
        Met à jour les informations d'un événement
        Modifie son nom, son contrat, son client, ses dates, son lieu, etc
        """
        try:
            event = self.event_repo.get_events(event_id)
            if not event:
                logging.debug(f"Événement introuvable : {event_id}")
                return {"error": "Événement introuvable"}

            updated_event = self.event_repo.update_event(
                event_id, name, start_date, end_date, location, attendees,
                contact, user_id, notes
            )
            return updated_event

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la mise à jour de l'événement "
                          f"{event_id}: {str(e)}")
            return {"error": "Erreur interne"}

    @require_permission("delete_event", check_ownership=False)
    def delete_event(self, event_id: int):
        """
        Supprime un événement par son ID.
        Retourne une erreur si l'événement n'existe pas.
        """
        try:
            event = self.event_repo.get_events(event_id)
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
