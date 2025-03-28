import os
import sentry_sdk

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

sentry_sdk.init(
    dsn="https://d25274d49594994e87a357fda009f962@o4509044061437952.ingest.de.sentry.io/4509044064649296",  # noqa: E501
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info  # noqa: E501
    send_default_pii=True,
)

# Récupérer la clé secrète pour JWT depuis le fichier .env
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("La clé secrète 'SECRET_KEY' doit être définie dans le "
                     "fichier .env")

# Base de données pour la création des classes
Base = declarative_base()

# Configuration de la connexion à la base de données
DATABASE_URL = "postgresql://admin:admin@127.0.0.1:5432/epic_events_crm_db"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
