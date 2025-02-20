from datetime import date
from sqlalchemy.orm import Session

from models.client import Client
from models.user import User


class ClientRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_client(self, full_name: str, email: str, phone: str,
                      company_name: str, contact: str) -> Client:
        """ Ajoute un nouveau client dans la base de données """

        user = self.db.query(User).filter(User.full_name == contact).first()

        new_client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company_name=company_name,
            contact=user.full_name if user else None,
            user_id=user.id if user else None
        )

        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        return new_client

    def get_client_by_id(self, client_id: int) -> Client:
        """ Récupère un client par son ID """
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_client_by_email(self, email: str) -> Client:
        """ Récupère un client par son adresse email """
        return self.db.query(Client).filter(Client.email == email).first()

    def update_client(self, client_id: int, full_name: str = None,
                      email: str = None, phone: str = None,
                      company_name: str = None, contact: str = None) -> Client:
        """
        Met à jour les informations d'un client.
        Modifie son nom, email, téléphone, entreprise ou contact.
        """
        client = self.get_client_by_id(client_id)
        if client:
            if full_name:
                client.full_name = full_name
            if email:
                client.email = email
            if phone:
                client.phone = phone
            if company_name:
                client.company_name = company_name
            if contact:
                client.contact = contact
                user = self.db.query(User).filter(
                    User.full_name == contact).first()
                client.user_id = user.id if user else None

            client.last_update_date = date.today()
            self.db.commit()
            self.db.refresh(client)
        return client

    def delete_client(self, client_id: int) -> bool:
        """ Supprime un client par son ID """
        client = self.get_client_by_id(client_id)
        if client:
            self.db.delete(client)
            self.db.commit()
            return True
        return False
