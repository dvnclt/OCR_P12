import logging

from sqlalchemy.exc import SQLAlchemyError

from utils.jwt_utils import create_access_token
from utils.utils import is_email_valid
from repositories.user_repository import UserRepository
from services.auth_service import clear_token, verify_password, set_password  # noqa: E501


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, email: str, password: str):
        """
        Vérifie l'email et le mot de passe de l'utilisateur.
        Retourne l'objet User si l'authentification réussit.
        Sinon, retourne None.
        """
        try:
            user = self.user_repo.get_user_by_email(email)

            if not user:
                logging.debug(f"Échec d'authentification pour {email} : "
                              "Utilisateur introuvable.")
                return {"error": "Utilisateur introuvable"}

            if not verify_password(user.hashed_password, password):
                logging.debug(f"Échec d'authentification pour {email} : "
                              "Mot de passe incorrect.")
                return {"error": "Mot de passe incorrect"}

            token = create_access_token(data={"sub": str(user.id)})

            return token

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de l'authentification pour {email}: "
                          f"{str(e)}")
            return {"error": "Erreur interne"}

    def logout(self):
        """
        Invalide le token JWT en le supprimant.
        Retourne un message de confirmation.
        """
        try:
            clear_token()

            logging.info("Utilisateur déconnecté")
            return {"message": "Utilisateur déconnecté"}

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la déconnexion : {str(e)}")
            return {"error": "Erreur interne"}

    def create_user(self, full_name: str, email: str, password: str,
                    role_id: int):
        """
        Vérifie les permissions du user
        Vérifie le format de l'adresse email
        Vérifie qu'elle 'n'existe pas déjà
        Hash le mdp
        Crée un nouvel utilisateur
        """
        try:
            if not is_email_valid(email):
                logging.debug(f"Adresse email invalide : {email}")
                return {"error": "Format d'email invalide"}

            existing_user = self.user_repo.get_user_by_email(email)
            if existing_user:
                logging.debug(f"Adresse email déjà existante : {email}")
                return {"error": "Cet adresse email est déjà utilisée"}

            hashed_password = set_password(password)
            new_user = self.user_repo.create_user(
                full_name,
                email,
                hashed_password,
                role_id
                )
            return new_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la création de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}

    def get_user_by_id(self, user_id: int):
        """
        Récupère un utilisateur par son ID après vérification des permissions.
        """
        try:
            existing_user = self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                logging.debug(f"Utilisateur introuvable avec l'ID {user_id}")
                return {"error": "Utilisateur introuvable"}

            return existing_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}

    def get_user_by_email(self, email: str):
        """
        Récupère un utilisateur par son email si permission.
        Retourne une erreur si l'email n'existe pas.
        """
        try:
            existing_user = self.user_repo.get_user_by_email(email)
            if not existing_user:
                logging.debug(f"Utilisateur introuvable depuis : {email}")
                return {"error": "Utilisateur introuvable"}

            return existing_user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur "
                          f"{email} : {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def get_user_by_name(self, full_name: str):
        """
        Récupère un utilisateur par son nom
        Retourne une erreur si n'existe pas.
        """
        try:
            existing_user = self.user_repo.get_user_by_name(full_name)
            if not existing_user:
                logging.debug(f"Utilisateur introuvable depuis : {full_name}")
                return {"error": "Utilisateur introuvable"}

            return existing_user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur "
                          f"{full_name} : {str(e)}")
            return {"error": "Erreur interne du serveur"}

    def update_user(self, user_id: str, full_name: str = None,
                    email: str = None, password: str = None,
                    role_id: int = None):
        """
        Met à jour les informations d'un utilisateur.
        Modifie son nom, email ou mot de passe.
        """
        try:
            existing_user = self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                logging.debug(f"Utilisateur introuvable ID : {user_id}")
                return {"error": "Utilisateur introuvable"}

            if password:
                password = set_password(password)

            updated_user = self.user_repo.update_user(
                user_id=existing_user.id,
                full_name=full_name,
                email=email,
                password=password,
                role_id=role_id
                )
            return updated_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la mise à jour de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}

    def delete_user(self, user_id: int):
        """Supprime un utilisateur par son ID si permission."""
        try:
            existing_user = self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                logging.debug(f"Utilisateur introuvable avec l'ID {user_id}")
                return {"error": "Utilisateur introuvable"}

            success = self.user_repo.delete_user(user_id)
            if success:
                return {"message": "Utilisateur supprimé"}
            else:
                return {"error": "Erreur lors de la suppression de "
                        "l'utilisateur"}

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la suppression de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}
