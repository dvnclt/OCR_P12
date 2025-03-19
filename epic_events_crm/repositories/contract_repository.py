from sqlalchemy.orm import Session
from models.contract import Contract
from models.user import User
from sqlalchemy import func
from decimal import Decimal


class ContractRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_contract(self, client_id: int, total_amount: float,
                        status: str, contact: str) -> Contract:
        """Ajoute un nouveau contrat dans la base de données."""

        user = self.db.query(User).filter(User.full_name == contact).first()

        new_contract = Contract(
            client_id=client_id,
            total_amount=(total_amount),
            paid_amount=0.0,
            remaining_amount=(total_amount),
            status=status,
            contact=contact,
            user_id=user.id if user else None
        )

        self.db.add(new_contract)
        self.db.commit()
        self.db.refresh(new_contract)
        return new_contract

    def get_contracts(self, contract_id: str = None,
                      user_id: int = None,
                      client_id: int = None,
                      status: str = None,
                      remaining_amount: bool = False
                      ) -> list[Contract]:
        """Récupère les contrats en fonction des filtres fournis"""

        query = self.db.query(Contract)

        if contract_id:
            query = query.filter(Contract.id == contract_id)
        if user_id:
            query = query.filter(Contract.user_id == user_id)
        if client_id:
            query = query.filter(Contract.client_id == client_id)
        if status:
            query = query.filter(func.lower(Contract.status) == status.lower())
        if remaining_amount:
            query = query.filter(Contract.remaining_amount != 0)

        return query.all()

    def update_contract(self, contract: Contract,
                        total_amount: float = None,
                        paid_amount: float = None,
                        status: str = None,
                        contact: str = None) -> Contract:
        """Met à jour les informations d'un contrat."""

        if total_amount is not None:
            contract.total_amount = Decimal(str(total_amount))
            contract.remaining_amount = (
                contract.total_amount - contract.paid_amount
                )
        if paid_amount is not None:
            contract.paid_amount += Decimal(str(paid_amount))
            contract.remaining_amount = (
                contract.total_amount - contract.paid_amount
                )
        if status is not None:
            contract.status = status
        if contact is not None:
            user = self.db.query(User).filter(
                User.email == contact
                ).first()
            contract.contact = contact
            contract.user_id = user.id if user else None

        self.db.commit()
        self.db.refresh(contract)
        return contract

    def delete_contract(self, contract_id: str) -> bool:
        """Supprime un contrat par son ID."""
        contract = self.get_contracts(contract_id)[0]
        if contract:
            self.db.delete(contract)
            self.db.commit()
            return True
        return False
