import logging

from sqlalchemy.exc import SQLAlchemyError

from repositories.user_repository import UserRepository
from services.auth_service import verify_password, set_password, require_permission  # noqa: E501


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
                logging.warning(f"Échec d'authentification pour {email} : "
                                "Utilisateur introuvable.")
                return None

            if not verify_password(user.hashed_password, password):
                logging.warning(f"Échec d'authentification pour {email} : "
                                "Mot de passe incorrect.")
                return None

            return user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de l'authentification pour {email}: "
                          f"{str(e)}")
            return None

    @require_permission("create_user")
    def create_user(self, user, full_name: str, email: str, password: str,
                    role_id: int):
        """
        Vérifie les permissions du user
        Vérifie que l'adresse email n'existe pas déjà
        Hash le mdp
        Crée un nouvel utilisateur
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

    @require_permission("read_user")
    def get_user_by_id(self, user, user_id: int):
        """
        Récupère un utilisateur par son ID après vérification des permissions.
        """
        try:
            existing_user = self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                logging.warning(f"Utilisateur introuvable avec l'ID {user_id}")
                return {"error": "Utilisateur introuvable"}, 404

            return existing_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}, 500

    @require_permission("read_user")
    def get_user_by_name(self, user, full_name: str):
        """
        Récupère un user par son nom complet après vérification des
        permissions.
        """
        try:
            existing_user = self.user_repo.get_user_by_name(full_name)
            if not existing_user:
                logging.warning("Utilisateur introuvable avec le nom "
                                f"{full_name}")
                return {"error": "Utilisateur introuvable"}, 404

            return existing_user

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la récupération de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}, 500

    @require_permission("read_user")
    def get_user_by_email(self, user, email: str):
        """
        Récupère un utilisateur par son email si permission.
        Retourne une erreur si l'email n'existe pas.
        """
        try:
            existing_user = self.user_repo.get_user_by_email(email)
            if not existing_user:
                logging.warning(f"Utilisateur introuvable depuis : {email}")
                return {"error": "Utilisateur introuvable"}, 404

            return existing_user

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la récupération de l'utilisateur "
                          f"{email} : {str(e)}")
            return {"error": "Erreur interne du serveur"}, 500

    @require_permission("update_user")
    def update_user(self, user, user_id: int, full_name: str = None,
                    email: str = None, password: str = None,
                    role_id: int = None):
        """
        Met à jour les informations d'un utilisateur.
        Modifie son nom, email ou mot de passe.
        """
        try:
            existing_user = self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                logging.warning(f"Utilisateur introuvable avec l'ID {user_id}")
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

    @require_permission("delete_user")
    def delete_user(self, user, user_id: int):
        """Supprime un utilisateur par son ID si permission."""
        try:
            existing_user = self.user_repo.get_user_by_id(user_id)
            if not existing_user:
                logging.warning(f"Utilisateur introuvable avec l'ID {user_id}")
                return {"error": "Utilisateur introuvable"}, 404

            success = self.user_repo.delete_user(user_id)
            if success:
                return {"message": "Utilisateur supprimé"}, 200
            else:
                return {"error": "Erreur lors de la suppression de "
                        "l'utilisateur"}, 500

        except SQLAlchemyError as e:
            logging.error("Erreur lors de la suppression de l'utilisateur : "
                          f"{str(e)}")
            return {"error": "Erreur interne"}, 500
