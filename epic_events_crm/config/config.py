from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base de données pour la création des classes
Base = declarative_base()

# Configuration de la connexion à la base de données
DATABASE_URL = "postgresql://admin:admin@127.0.0.1:5432/epic_events_crm_db"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
