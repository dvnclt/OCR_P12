from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la connexion à la base de données
DATABASE_URL = "postgresql://admin:admin@127.0.0.1:5432/epic_events_crm_db"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base de données pour la création des classes
Base = declarative_base()

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
