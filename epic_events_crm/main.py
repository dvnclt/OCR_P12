from config.config import Base, engine
import models  # noqa: F401  # type: ignore


if __name__ == '__main__':
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées")
