import logging

from sqlalchemy.exc import SQLAlchemyError

from repositories.user_repository import UserRepository
from services.auth_service import verify_password, set_password


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, full_name: str, email: str, password: str,
                    role_id: int):
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
            return {"error": "Erreur interne"}, 500

    def get_user_by_id(self, user_id: int):
        """
        Récupère un utilisateur par son ID.
        Retourne une erreur si l'utilisateur n'existe pas.
        """
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                logging.warning("Utilisateur introuvable")
                return {"error": "Utilisateur introuvable"}, 404
            return user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur "
                          f"{user_id} : {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def get_user_by_name(self, full_name: str):
        """
        Récupère un user par son nom complet.
        Retourne une erreur si le user n'existe pas.
        """
        try:
            user = self.user_repo.get_user_by_name(full_name)
            if not user:
                logging.warning(f"Utilisateur introuvable : {full_name}")
                return {"error": "Utilisateur introuvable"}, 404
            return user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération de l'utilisateur "
                          f"avec le nom {full_name}: {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def get_user_by_email(self, email: str):
        """
        Récupère un utilisateur par son email.
        Retourne une erreur si l'email n'existe pas.
        """
        try:
            user = self.user_repo.get_user_by_email(email)
            if not user:
                logging.warning(f"Utilisateur introuvable depuis : {email}")
                return {"error": "Utilisateur introuvable"}, 404
            return user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur "
                          f"{email} : {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    def update_user(self, user_id: int, full_name: str = None,
                    email: str = None, password: str = None,
                    role_id: int = None):
        """
        Met à jour les informations d'un utilisateur.
        Modifie son nom, email ou mot de passe.
        """
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                logging.warning("Utilisateur introuvable")
                return {"error": "Utilisateur introuvable"}, 404

            if password:
                password = set_password(password)

            updated_user = self.user_repo.update_user(
                user_id, full_name, email, password, role_id)
            return updated_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la mise à jour de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}, 500

    def delete_user(self, user_id: int):
        """Supprime un utilisateur par son ID."""
        try:
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                logging.warning("Utilisateur introuvable")
                return {"error": "Utilisateur introuvable"}, 404

            success = self.user_repo.delete_user(user_id)
            if success:
                return {"message": "Utilisateur supprimé"}, 200
            else:
                return {"error": "Erreur lors de la suppression de "
                        "l'utilisateur"}, 500

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la suppression de l'utilisateur "
                          f": {str(e)}")
            return {"error": "Erreur interne"}, 500

    def authenticate(self, email: str, password: str):
        """
        Vérifie l'email et le mot de passe de l'utilisateur.
        Retourne l'utilisateur si l'authentification réussit, sinon None.
        """
        try:
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

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de l'authentification pour {email}: "
                          f"{str(e)}")
            return {"error": "Erreur interne du serveur"}, 500
