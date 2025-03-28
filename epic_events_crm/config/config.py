import os
import sentry_sdk
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

""" Chargement des variables d'environnement depuis le fichier .env """
load_dotenv()


""" Initialisation de Sentry pour le suivi des erreurs """
sentry_sdk.init(
    dsn="https://d25274d49594994e87a357fda009f962@o4509044061437952.ingest.de.sentry.io/4509044064649296",  # noqa: E501
    send_default_pii=True,
    )


def handle_exception(exc_type, exc_value, exc_traceback):
    """ Définition du gestionnaire global pour les exceptions non interceptées """  # noqa: E501
    if issubclass(exc_type, KeyboardInterrupt):  # Exclu la capture des exceptions KeyboardInterrupt # noqa: E501
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    # Afficher un message d'erreur propre
    print(f"Une erreur est survenue : {exc_value}")

    # Envoyer l'exception à Sentry
    event_id = sentry_sdk.capture_exception(exc_value)
    if event_id:
        print("[Sentry] L'événement a été envoyé avec succès.")
        print(f"Event ID : {event_id}")
    else:
        print("[Sentry] Échec de l'envoi de l'événement.")


# Remplace le gestionnaire d'exceptions par défaut
sys.excepthook = handle_exception


""" Récupération de la clé secrète pour JWT depuis le fichier .env """
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("La clé secrète 'SECRET_KEY' doit être définie dans le "
                     "fichier .env")


""" Définition de la configuration des accès à la base de données """
# Base de données pour la création des classes
Base = declarative_base()
# Configuration de la connexion à la base de données
DATABASE_URL = "postgresql://admin:admin@127.0.0.1:5432/epic_events_crm_db"
# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)
# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
