from sqlalchemy.orm import sessionmaker

from config.config import Base, engine
from models import user, client, contract, event  # noqa: F401
from epic_events_crm.config.init_permissions import initialize_roles_and_permissions  # noqa: E501


# Crée la session
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées")

    # Initialiser les rôles et les permissions
    initialize_roles_and_permissions(session)

    # Fermer la session après l'initialisation
    session.close()
