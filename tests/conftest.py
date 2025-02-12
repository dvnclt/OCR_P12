import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import Base  # type: ignore
from models import user, role, client, contract, event  # noqa: F401, E501, # type: ignore

# Création d'une base de données SQLite en mémoire pour les tests
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


@pytest.fixture
def db_session():
    """
    Fixture qui démarre une transaction et annule toutes les modifications
    après chaque test.
    """
    Base.metadata.create_all(bind=engine)  # Crée les tables avant chaque test
    connection = engine.connect()  # Créé une connexion indépendante

    session = TestingSessionLocal(bind=connection)
    yield session  # Fournit la session aux tests

    session.rollback()  # Annule les modifications
    connection.close()  # Ferme la connexion
    Base.metadata.drop_all(bind=engine)  # Supprime les tables après le test
