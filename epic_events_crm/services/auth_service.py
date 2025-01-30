from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def set_password(self, password: str):
    # Hash le mot de passe avant de le stocker
    self.hashed_password = pwd_context.hash(password)


def verify_password(self, password: str):
    # Vérifie si le mot de passe correspond au hash stocké
    return pwd_context.verify(password, self.hashed_password)
