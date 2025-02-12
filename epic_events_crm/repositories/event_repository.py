from sqlalchemy.orm import Session

from models.event import Event
from models.client import Client
from models.contract import Contract
from models.user import User


class EventRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_event(self, name: str, contract_id: int, client_id: int,
                     start_date: str, end_date: str, location: str,
                     attendees: int, contact: str, user_id: int,
                     notes: str) -> Event:
        """Ajoute un nouvel événement à la base de données."""

        new_event = Event(
            name=name,
            contract_id=contract_id,
            client_id=client_id,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
            contact=contact,
            user_id=user_id,
            notes=notes
        )

        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return new_event

    def get_event_by_id(self, event_id: int) -> Event:
        """Récupère un événement par son ID."""
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_events_by_contract_id(self, contract_id: int) -> list[Event]:
        """Récupère tous les événements associés à un contrat donné."""
        return self.db.query(Event).filter(
            Event.contract_id == contract_id
            ).all()

    def get_events_by_client_id(self, client_id: int) -> list[Event]:
        """Récupère tous les événements associés à un client donné."""
        return self.db.query(Event).filter(
            Event.client_id == client_id
            ).all()

    def get_events_by_user_id(self, user_id: int) -> list[Event]:
        """Récupère tous les événements associés à un utilisateur donné."""
        return self.db.query(Event).filter(Event.user_id == user_id).all()

    def update_event(self, event_id: int, name: str = None,
                     contract_id: int = None, client_id: int = None,
                     start_date: str = None, end_date: str = None,
                     location: str = None, attendees: int = None,
                     contact: str = None, user_id: int = None,
                     notes: str = None) -> Event:
        """Met à jour un événement existant dans la base de données."""

        event = self.get_event_by_id(event_id)
        if event:
            if name:
                event.name = name
            if contract_id:
                event.contract_id = contract_id
                event.contract = self.db.query(Contract).filter(
                    Contract.id == contract_id
                    ).first()
            if client_id:
                event.client_id = client_id
                event.client = self.db.query(Client).filter(
                    Client.id == client_id
                    ).first()
            if start_date:
                event.start_date = start_date
            if end_date:
                event.end_date = end_date
            if location:
                event.location = location
            if attendees:
                event.attendees = attendees
            if contact:
                event.contact = contact
            if user_id:
                event.user_id = user_id
                event.user = self.db.query(User).filter(
                    User.id == user_id
                    ).first()
            if notes:
                event.notes = notes

            self.db.commit()
            self.db.refresh(event)
        return event

    def delete_event(self, event_id: int) -> bool:
        """Supprime un événement par son ID."""
        event = self.get_event_by_id(event_id)
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False
