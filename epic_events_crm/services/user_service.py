import logging

from sqlalchemy.exc import SQLAlchemyError

from utils.jwt_utils import create_access_token
from repositories.user_repository import UserRepository
from utils.auth_utils import clear_token, verify_password, set_password  # noqa: E501
from utils.permission_utils import require_permission


class UserService:
    def __init__(self, user_repo: UserRepository):
        """
        Initialisation du service

        Args:
            user_repo (UserRepository): Instance de UserRepository
        """
        self.user_repo = user_repo

    def authenticate(self, email: str, password: str):
        """
        Authentification d'un utilisateur

        Args:
            email (str): Email de l'utilisateur
            password (str): Mot de passe de l'utilisateur

        Returns:
            str or dict: Token si succès sinon message d'erreur.

        Raises:
            SQLAlchemyError: En cas d'erreur avec la base de données.
        """
        try:
            # Recherche l'user
            user = self.user_repo.get_user_by_email(email)

            # Erreur si email non trouvé
            if not user:
                logging.debug(f"Échec d'authentification pour {email} : "
                              "Utilisateur introuvable.")
                return {"error": "Utilisateur introuvable"}

            # Erreur si mdp ne correspond pas
            if not verify_password(user.hashed_password, password):
                logging.debug(f"Échec d'authentification pour {email} : "
                              "Mot de passe incorrect.")
                return {"error": "Mot de passe incorrect"}

            # Créé un token
            token = create_access_token(data={"sub": str(user.id)})

            return token

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de l'authentification pour {email}: "
                          f"{str(e)}")
            return {"error": "Erreur interne"}

    def logout(self):
        """
        Déconnexion d'un utilisateur

        Returns:
            dict: Message de confirmation

        Raises:
            SQLAlchemyError: En cas d'erreur avec la base de données
        """
        try:
            # Supprime le token
            clear_token()

            # Confirme la déconnexion
            logging.info("Utilisateur déconnecté")
            return {"message": "Utilisateur déconnecté"}

        except SQLAlchemyError as e:
            logging.error(f"Erreur lors de la déconnexion : {str(e)}")
            return {"error": "Erreur interne"}

    @require_permission("create_user", check_ownership=False)
    def create_user(self, full_name: str, email: str, password: str,
                    role_id: int):
        """
        Créer un utilisateur

        Args:
            full_name (str): Nom complet de l'utilisateur
            email (str): Adresse email de l'utilisateur
            password (str): Mot de passe non chiffré de l'utilisateur
            role_id (int): Identifiant du rôle associé à l'utilisateur

        Returns:
            User: Objet utilisateur créé si opération réussie
            dict: Message d'erreur en cas d'échec

        Raises:
            SQLAlchemyError: En cas d'erreur avec la base de données
        """
        try:
            # Vérifie que l'user n'existe pas déjà
            existing_user = self.user_repo.get_user_by_email(email)
            if existing_user:
                logging.debug(f"Adresse email déjà existante : {email}")
                return {"error": "Cet adresse email est déjà utilisée"}

            # Hash le password
            hashed_password = set_password(password)

            # Créé le user
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

    @require_permission("read_user", check_ownership=False)
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

    @require_permission("read_user", check_ownership=False)
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

    @require_permission("read_user", check_ownership=False)
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

    @require_permission("update_user", check_ownership=False)
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

    @require_permission("delete_user", check_ownership=False)
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
