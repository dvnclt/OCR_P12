import logging
from sqlalchemy.exc import SQLAlchemyError

from epic_events_crm.repositories.user_repository import UserRepository
from epic_events_crm.services.auth_service import verify_password, set_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, email: str, full_name: str, password: str):
        """
        Crée un nouvel utilisateur
        Vérifie que l'adresse email n'existe pas déjà
        Hash le mdp
        """
        try:
            existing_user = self.user_repo.get_user_by_email(email)
            if existing_user:
                logging.warning(f"Adresse email déjà existante : {email}")
                return {"error": "Cet adresse email est déjà utilisée"}, 400

            hashed_password = set_password(password)
            new_user = self.user_repo.create_user(email, full_name,
                                                  hashed_password)
            return new_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la création de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}, 500

    def get_user_by_id(self, user_id: int):
        """
        Récupère un utilisateur par son ID.
        Retourne une erreur si l'utilisateur n'existe pas.
        """
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                logging.warning(f"Utilisateur introuvable depuis : {user_id}")
                return {"error": "Utilisateur introuvable"}, 404

            return user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur "
                          f"{user_id} : {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def authenticate(self, email: str, password: str):
        """
        Vérifie l'email et le mot de passe de l'utilisateur.
        Retourne l'utilisateur si l'authentification réussit, sinon None.
        """
        user = self.user_repo.get_user_by_email(email)

        if not user:
            logging.warning(f"Échec d'authentification pour {email} : "
                            "Utilisateur introuvable.")
            return {"error": "Utilisateur introuvable"}, 404

        if not verify_password(user.hashed_password, password):
            logging.warning(f"Échec d'authentification pour {email} : "
                            "Mot de passe incorrect.")
            return {"error": "Mot de passe incorrect"}, 401

        return user
