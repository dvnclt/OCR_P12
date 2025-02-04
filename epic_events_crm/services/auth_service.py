from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def set_password(password: str) -> str:
    # Hash le mot de passe avant de le stocker
    return pwd_context.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    # Vérifie si le mot de passe correspond au hash stocké
    return pwd_context.verify(password, hashed_password)
