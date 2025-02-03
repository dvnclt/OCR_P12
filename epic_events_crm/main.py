from config.config import Base, engine
from models import user, client, contract, event  # noqa: F401


if __name__ == '__main__':
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées")
