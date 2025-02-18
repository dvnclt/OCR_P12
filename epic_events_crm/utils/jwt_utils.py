import jwt
import datetime

from typing import Optional
from config.config import SECRET_KEY
from repositories.user_repository import UserRepository

# Définir la durée d'expiration par défaut du token
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Fonction pour générer un token JWT
def create_access_token(data: dict,
                        expires_delta: Optional[datetime.timedelta] = None) -> str:  # noqa: E501
    to_encode = data.copy()

    # Si une durée d'expiration est définie, on l'ajoute
    # Sinon on utilise la valeur par défaut
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode.update({"exp": expire})

    # Générer le JWT avec la clé secrète
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


# Fonction pour vérifier un token JWT et récupérer un User
def get_current_user(token: str, user_repo: UserRepository) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            return None

        user = user_repo.get_user_by_id(user_id)
        return user
    except jwt.ExpiredSignatureError:
        print("Le token a expiré")
        return None
    except jwt.InvalidTokenError:
        print("Token invalide")
        return None
