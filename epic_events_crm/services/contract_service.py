import logging
from sqlalchemy.exc import SQLAlchemyError

from repositories.contract_repository import ContractRepository
from models.client import Client
from services.auth_service import require_permission


class ContractService:
    def __init__(self, contract_repo: ContractRepository):
        self.contract_repo = contract_repo

    @require_permission("create_contract")
    def create_contract(self, client_id: int, contract_amount: float,
                        contract_status: str, contact: str):
        """
        Crée un nouveau contrat dans la base de données.
        Vérifie que le client existe avant de créer le contrat.
        """
        try:
            client = self.contract_repo.db.query(Client).filter(
                Client.id == client_id
                ).first()
            if not client:
                logging.warning(f"Client introuvable : {client_id}")
                return {"error": "Client introuvable"}, 404

            new_contract = self.contract_repo.create_contract(
                client_id, contract_amount, contract_status, contact
            )
            return new_contract

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la création du contrat : {str(e)}")
            return {"error": "Erreur interne"}, 500

    @require_permission("read_contract")
    def get_contract_by_id(self, contract_id: int):
        """
        Récupère un contrat par son ID.
        Retourne une erreur si le contrat n'existe pas.
        """
        try:
            contract = self.contract_repo.get_contract_by_id(contract_id)
            if not contract:
                logging.warning(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}, 404
            return contract

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération du contrat "
                          f"{contract_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("read_contract")
    def get_contracts_by_client(self, client_id: int):
        """
        Récupère tous les contrats liés à un client donné.
        Retourne une erreur si aucun contrat n'est trouvé.
        """
        try:
            contracts = self.contract_repo.get_contracts_by_client_id(
                client_id
                )
            if not contracts:
                logging.warning(f"Aucun contrat trouvé pour le client "
                                f"{client_id}")
                return {"error": "Aucun contrat trouvé"}, 404
            return contracts

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des contrats du "
                          f"client {client_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("read_contract")
    def get_contracts_by_user(self, user_id: int):
        """
        Récupère tous les contrats assignés à un utilisateur donné.
        Retourne une erreur si aucun contrat n'est trouvé.
        """
        try:
            contracts = self.contract_repo.get_contracts_by_user_id(user_id)
            if not contracts:
                logging.warning(f"Aucun contrat trouvé pour l'utilisateur "
                                f"{user_id}")
                return {"error": "Aucun contrat trouvé"}, 404
            return contracts

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des contrats de "
                          f"l'utilisateur {user_id}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("update_contract")
    def update_contract(self, contract_id: int,
                        contract_amount: float = None,
                        remaining_amount: float = None,
                        contract_status: str = None, contact: str = None):
        """
        Met à jour les informations d'un contrat.
        Modifie son montant, son statut, son contact ou le montant restant.
        """
        try:
            contract = self.contract_repo.get_contract_by_id(contract_id)
            if not contract:
                logging.warning(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}, 404

            updated_contract = self.contract_repo.update_contract(
                contract_id, contract_amount, remaining_amount,
                contract_status, contact
            )
            return updated_contract

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la mise à jour du contrat "
                          f"{contract_id} : {str(e)}")
            return {"error": "Erreur interne"}, 500

    @require_permission("update_contract")
    def record_payment(self, contract_id: int, payment_amount: float):
        """
        Effectue un paiement et met à jour le montant restant du contrat.
        """
        try:
            contract = self.contract_repo.get_contract_by_id(contract_id)
            if not contract:
                logging.warning(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}, 404

            if payment_amount <= 0:
                logging.warning("Montant de paiement invalide : "
                                f"{payment_amount}")
                return {"error": "Le paiement doit être positif"}, 400

            if payment_amount > contract.remaining_amount:
                logging.warning(f"Paiement trop élevé ({payment_amount}€) pour"
                                f" un reste de {contract.remaining_amount}€")
                return {"error": "Le paiement dépasse le montant restant"}, 400

            new_remaining_amount = contract.remaining_amount - payment_amount

            updated_contract = self.contract_repo.update_contract(
                contract_id,
                remaining_amount=new_remaining_amount
            )

            return updated_contract

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de l'enregistrement du paiement : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}, 500

    @require_permission("delete_contract")
    def delete_contract(self, contract_id: int):
        """
        Supprime un contrat par son ID.
        Retourne une erreur si le contrat n'existe pas.
        """
        try:
            contract = self.contract_repo.get_contract_by_id(contract_id)
            if not contract:
                logging.warning(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}, 404

            success = self.contract_repo.delete_contract(contract_id)
            if success:
                return {"message": "Contrat supprimé"}, 200
            else:
                return {"error": "Erreur lors de la suppression"}, 500

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la suppression du contrat "
                          f"{contract_id} : {str(e)}")
            return {"error": "Erreur interne"}, 500
