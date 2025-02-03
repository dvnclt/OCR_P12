import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import Base  # type: ignore
from models import user, client, contract, event  # noqa: F401, # type: ignore

# Création d'une base de données SQLite en mémoire pour les tests
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


# Fixture pour fournir une session de base de données pour les tests.
@pytest.fixture
def db_session():
    # Crée toutes les tables dans la BDD en mémoire
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()

    # Supprime les tables après le test
    Base.metadata.drop_all(bind=engine)
