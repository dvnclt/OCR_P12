import logging
import uuid
from sqlalchemy.exc import SQLAlchemyError

from repositories.contract_repository import ContractRepository
from models.client import Client
from utils.permission_utils import require_permission


class ContractService:
    def __init__(self, contract_repo: ContractRepository, user_repo=None):
        self.contract_repo = contract_repo
        self.user_repo = user_repo

    @require_permission("create_contract", check_ownership=False)
    def create_contract(self, client_id: int, total_amount: float,
                        status: str, contact: str):
        """
        Crée un nouveau contrat dans la base de données.
        Vérifie que le client existe avant de créer le contrat.
        """
        try:
            client = self.contract_repo.db.query(Client).filter(
                Client.id == client_id
                ).first()
            if not client:
                logging.debug(f"Client introuvable : {client_id}")
                return {"error": "Client introuvable"}

            new_contract = self.contract_repo.create_contract(
                client_id, total_amount, status, contact
            )
            return new_contract

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la création du contrat : {str(e)}")
            return {"error": "Erreur interne"}

    @require_permission("read_contract", check_ownership=False)
    def get_contracts(self, contract_id: str = None,
                      user_id: int = None,
                      client_id: int = None,
                      status: str = None,
                      remaining_amount: bool = False,
                      ):
        """
        Récupère les contrats selon les critères fournis
        Retourne une erreur si aucun contrat n'est trouvé
        """
        try:
            if contract_id is not None:
                try:
                    uuid_obj = uuid.UUID(contract_id)  # noqa: F841
                except ValueError:
                    return {"error": "ID du contrat invalide"}
            contracts = self.contract_repo.get_contracts(contract_id=contract_id,  # noqa: E501
                                                         user_id=user_id,
                                                         client_id=client_id,
                                                         status=status,
                                                         remaining_amount=remaining_amount,  # noqa: E501
                                                         )

            if not contracts:
                logging.debug("Aucun contrat trouvé pour les critères : "
                              f"contract_id={contract_id}",
                              f"user_id={user_id}",
                              f"client_id={client_id}",
                              f"status={status}",
                              f"remaining_amount={remaining_amount}"
                              )
                return {"error": "Aucun contrat trouvé"}

            return contracts

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération des contrats : "
                          f"{str(e)}")
            return {"error": "Erreur interne du serveur"}

    @require_permission("update_contract", check_ownership=False)
    def update_contract(self, contract_id: int,
                        contact: str = None,
                        total_amount: float = None,
                        paid_amount: float = None,
                        status: str = None,
                        ):
        """
        Met à jour les informations d'un contrat
        Modifie son montant, son statut, son contact
        """
        try:
            contract = self.contract_repo.get_contracts(contract_id=contract_id)[0]  # noqa: E501
            if not contract:
                logging.debug(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}

            updated_contract = self.contract_repo.update_contract(
                contract, total_amount, paid_amount, status, contact
            )
            return updated_contract

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la mise à jour du contrat "
                          f"{id} : {str(e)}")
            return {"error": "Erreur interne"}

    @require_permission("delete_contract", check_ownership=False)
    def delete_contract(self, contract_id: str):
        """
        Supprime un contrat par son ID.
        Retourne une erreur si le contrat n'existe pas.
        """
        try:
            contract = self.contract_repo.get_contracts(contract_id)
            if not contract:
                logging.debug(f"Contrat introuvable : {contract_id}")
                return {"error": "Contrat introuvable"}

            success = self.contract_repo.delete_contract(contract_id)
            if success:
                return {"message": "Contrat supprimé"}
            else:
                return {"error": "Erreur lors de la suppression"}

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la suppression du contrat "
                          f"{contract_id} : {str(e)}")
            return {"error": "Erreur interne"}
