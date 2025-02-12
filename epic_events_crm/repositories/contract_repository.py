from sqlalchemy.orm import Session
from sqlalchemy import Numeric

from models.contract import Contract
from models.user import User


class ContractRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_contract(self, client_id: int, contract_amount: float,
                        contract_status: str, contact: str) -> Contract:
        """Ajoute un nouveau contrat dans la base de données."""

        user = self.db.query(User).filter(User.full_name == contact).first()

        new_contract = Contract(
            client_id=client_id,
            contract_amount=Numeric(contract_amount),
            remaining_amount=Numeric(contract_amount),
            contract_status=contract_status,
            contact=contact,
            user_id=user.id if user else None
        )

        self.db.add(new_contract)
        self.db.commit()
        self.db.refresh(new_contract)
        return new_contract

    def get_contract_by_id(self, contract_id: int) -> Contract:
        """Récupère un contrat par son ID."""
        return self.db.query(Contract).filter(
            Contract.id == contract_id
            ).first()

    def get_contracts_by_client_id(self, client_id: int) -> list[Contract]:
        """Récupère tous les contrats d'un client donné."""
        return self.db.query(Contract).filter(
            Contract.client_id == client_id
            ).all()

    def get_contracts_by_user_id(self, user_id: int) -> list[Contract]:
        """Récupère tous les contrats assignés à un utilisateur donné."""
        return self.db.query(Contract).filter(
            Contract.user_id == user_id
            ).all()

    def update_contract(self, contract_id: int, contract_amount: float = None,
                        remaining_amount: float = None,
                        contract_status: str = None,
                        contact: str = None) -> Contract:
        """Met à jour les informations d'un contrat."""

        contract = self.get_contract_by_id(contract_id)
        if contract:
            if contract_amount is not None:
                contract.contract_amount = Numeric(contract_amount)
            if remaining_amount is not None:
                contract.remaining_amount = Numeric(remaining_amount)
            if contract_status is not None:
                contract.contract_status = contract_status
            if contact is not None:
                user = self.db.query(User).filter(
                    User.full_name == contact
                    ).first()
                contract.contact = contact
                contract.user_id = user.id if user else None

            self.db.commit()
            self.db.refresh(contract)
        return contract

    def delete_contract(self, contract_id: int) -> bool:
        """Supprime un contrat par son ID."""
        contract = self.get_contract_by_id(contract_id)
        if contract:
            self.db.delete(contract)
            self.db.commit()
            return True
        return False
