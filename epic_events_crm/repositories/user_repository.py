from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, full_name: str, email: str,
                    hashed_password: str, role_id: int) -> User:
        """ Ajoute un nouvel utilisateur dans la db """
        new_user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password,
            role_id=role_id)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user_by_id(self, user_id: int) -> User:
        """ Récupère un utilisateur par son ID. """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        """ Récupère un utilisateur par son adresse email. """
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_name(self, full_name: str) -> User:
        """ Récupère un utilisateur par son nom complet. """
        return self.db.query(User).filter(User.full_name == full_name).all()

    def update_user(self, user_id: int, full_name: str = None,
                    email: str = None, password: str = None,
                    role_id: int = None) -> User:
        """
        Met à jour les informations d'un utilisateur.
        Modifie son nom, email ou mot de passe.
        """
        user = self.get_user_by_id(user_id)
        if user:
            if full_name:
                user.full_name = full_name
            if email:
                user.email = email
            if password:
                user.hashed_password = password
            if role_id:
                user.role_id = role_id
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        """ Supprime un utilisateur par son ID. """
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
