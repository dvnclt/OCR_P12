import pytest
from sqlalchemy.exc import IntegrityError

from repositories.client_repository import ClientRepository  # noqa: F401, E501,  # type: ignore
from models.user import User  # noqa: F401, E501,  # type: ignore


def test_create_client(db_session):
    """Test de création d'un client"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    new_client = repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    assert new_client is not None
    assert new_client.full_name == "Test Client"
    assert new_client.email == "client@example.com"
    assert new_client.phone == "123456789"
    assert new_client.company_name == "Test Company"
    assert new_client.contact == "Test User"
    assert new_client.user_id == user.id


def test_get_client_by_id(db_session):
    """Test de récupération d'un client par son ID"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    client = repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    retrieved_client = repo.get_client_by_id(client.id)

    assert retrieved_client is not None
    assert retrieved_client.id == client.id
    assert retrieved_client.full_name == client.full_name


def test_get_client_by_id_not_found(db_session):
    """Test de récupération d'un client inexistant par son ID"""
    repo = ClientRepository(db_session)
    client = repo.get_client_by_id(9999)
    assert client is None


def test_get_client_by_name(db_session):
    """Test de récupération d'un client par son nom"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    client = repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    retrieved_client = repo.get_client_by_name(client.full_name)
    assert retrieved_client is not None
    assert retrieved_client.full_name == "Test Client"


def test_get_client_by_name_not_found(db_session):
    """Test de récupération d'un client inexistant par son nom"""
    repo = ClientRepository(db_session)
    client = repo.get_client_by_name("Non Existent Client")
    assert client is None


def test_get_client_by_email(db_session):
    """Test de récupération d'un client par email"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    client = repo.get_client_by_email("client@example.com")

    assert client is not None
    assert client.email == "client@example.com"


def test_create_client_duplicate_email(db_session):
    """Test de la contrainte d'unicité de l'email dans la db"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    with pytest.raises(IntegrityError):
        repo.create_client(
            full_name="Other Client",
            email="client@example.com",
            phone="987654321",
            company_name="Other Company",
            contact="Other User"
        )


def test_get_client_by_email_not_found(db_session):
    """
    Test de récupération d'un client par email lorsque le client
    n'existe pas
    """
    repo = ClientRepository(db_session)

    client = repo.get_client_by_email("non_existent@example.com")
    assert client is None


def test_update_client(db_session):
    """Test de mise à jour d'un client"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    client = repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    updated_client = repo.update_client(
        client_id=client.id,
        full_name="Updated Client",
        email="updated_client@example.com",
        phone="987654321",
        company_name="Updated Company",
        contact="Updated User"
    )

    assert updated_client is not None
    assert updated_client.full_name == "Updated Client"
    assert updated_client.email == "updated_client@example.com"
    assert updated_client.phone == "987654321"
    assert updated_client.company_name == "Updated Company"


def test_update_client_not_found(db_session):
    """Test de mise à jour d'un client qui n'existe pas"""
    repo = ClientRepository(db_session)

    updated_client = repo.update_client(
        client_id=9999,
        full_name="Non Existent",
        email="non_existent@example.com",
        phone="000000000",
        company_name="Unknown Company",
        contact="Unknown User"
    )

    assert updated_client is None


def test_delete_client(db_session):
    """Test de suppression d'un client"""
    repo = ClientRepository(db_session)

    user = User(full_name="Test User", email="user@example.com")
    db_session.add(user)
    db_session.commit()

    client = repo.create_client(
        full_name="Test Client",
        email="client@example.com",
        phone="123456789",
        company_name="Test Company",
        contact="Test User"
    )

    deleted = repo.delete_client(client.id)
    assert deleted is True

    client_check = repo.get_client_by_id(client.id)
    assert client_check is None


def test_delete_client_not_found(db_session):
    """Test de suppression d'un client inexistant"""
    repo = ClientRepository(db_session)
    deleted = repo.delete_client(9999)
    assert deleted is False
