from sqlalchemy.orm import Session
from datetime import datetime

from models.event import Event
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

    def get_events(self, event_id: int = None,
                   contract_id: str = None,
                   client_id: int = None,
                   user_id: int = None,
                   start_date: datetime = None,
                   end_date: datetime = None,
                   no_user: bool = False,
                   ) -> list[Event]:
        """Récupère les évènements en fonction des filtres fournis"""

        query = self.db.query(Event)

        if event_id:
            query = query.filter(Event.id == event_id)
        if contract_id:
            query = query.filter(Event.contract_id == contract_id)
        if client_id:
            query = query.filter(Event.client_id == client_id)
        if user_id:
            query = query.filter(Event.user_id == user_id)
        if start_date:
            query = query.filter(Event.start_date == start_date)
        if end_date:
            query = query.filter(Event.end_date == end_date)
        if no_user:
            query = query.filter(Event.user_id.is_(None))

        return query.all()

    def update_event(self, event_id: int, name: str = None,
                     start_date: str = None, end_date: str = None,
                     location: str = None, attendees: int = None,
                     contact: str = None, user_id: int = None,
                     notes: str = None) -> Event:
        """Met à jour un événement existant dans la base de données."""

        event = self.get_events(event_id)[0]
        if event:
            if name:
                event.name = name
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
        event = self.get_events(event_id)[0]
        if event:
            self.db.delete(event)
            self.db.commit()
            return True
        return False
