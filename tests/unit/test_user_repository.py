import pytest
from sqlalchemy.exc import IntegrityError

from repositories.user_repository import UserRepository  # noqa: F401, E501,  # type: ignore


def test_create_user(db_session):
    """Test de création d'un utilisateur"""
    repo = UserRepository(db_session)

    new_user = repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd",
        role="gestion"
        )

    assert new_user is not None
    assert new_user.full_name == "Test User"
    assert new_user.email == "test@example.com"
    assert new_user.role == "gestion"


def test_get_user_by_id(db_session):
    """Test de récupération d'un utilisateur par son ID"""
    repo = UserRepository(db_session)

    user = repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd",
        role="gestion"
    )

    user_id = repo.get_user_by_id(user.id)

    assert user_id is not None
    assert user_id.id == user.id
    assert user_id.email == user.email
    assert user_id.full_name == user.full_name
    assert user_id.role == user.role


def test_get_user_by_id_not_found(db_session):
    """Test de récupération d'un utilisateur inexistant par son ID"""
    repo = UserRepository(db_session)

    user = repo.get_user_by_id(9999)
    assert user is None


def test_get_user_by_name(db_session):
    """Test de récupération d'un utilisateur par son nom complet """
    repo = UserRepository(db_session)

    user = repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd",
        role="gestion"
    )

    user_name = repo.get_user_by_name(user.full_name)

    assert user_name is not None
    assert user_name.id == user.id
    assert user_name.email == user.email
    assert user_name.full_name == user.full_name
    assert user_name.role == user.role


def test_get_user_by_name_not_found(db_session):
    """
    Test de récupération d'un utilisateur par son nom complet lorsque l'user
    n'existe pas
    """
    repo = UserRepository(db_session)

    user = repo.get_user_by_name("Jean Dupont")
    assert user is None


def test_get_user_by_email(db_session):
    """Test de récupération d'un utilisateur par email"""
    repo = UserRepository(db_session)

    repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd",
        role="gestion"
    )

    user = repo.get_user_by_email("test@example.com")

    assert user is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.role == "gestion"


def test_create_user_duplicate_email(db_session):
    """Test de la contrainte d'unicité de l'email dans la db"""
    repo = UserRepository(db_session)

    repo.create_user(email="test@example.com",
                     full_name="Test User",
                     hashed_password="hashedpwd",
                     role="gestion")

    with pytest.raises(IntegrityError):
        repo.create_user(email="test@example.com",
                         full_name="Other User",
                         hashed_password="anotherpwd",
                         role="commercial")


def test_get_user_by_email_not_found(db_session):
    """
    Test de récupération d'un utilisateur par email lorsque l'user
    n'existe pas
    """
    repo = UserRepository(db_session)

    user = repo.get_user_by_email("non_existent@example.com")
    assert user is None


def test_update_user(db_session):
    """Test de mise à jour d'un utilisateur"""
    repo = UserRepository(db_session)

    user = repo.create_user(
        email="test_user@example.com",
        full_name="Test User",
        hashed_password="hashedpwd",
        role="gestion"
    )

    updated_user = repo.update_user(
        user_id=user.id,
        full_name="Updated Name",
        email="updated_email@example.com",
        role="commercial"
    )

    assert updated_user is not None
    assert updated_user.full_name == "Updated Name"
    assert updated_user.email == "updated_email@example.com"
    assert updated_user.role == "commercial"


def test_update_user_not_found(db_session):
    """Test de mise à jour d'un utilisateur qui n'existe pas"""
    repo = UserRepository(db_session)

    updated_user = repo.update_user(
        user_id=9999,
        full_name="Non Existant",
        email="non_existant@example.com",
        role="gestion"
    )

    assert updated_user is None


def test_delete_user(db_session):
    """Test de suppression d'un utilisateur"""
    repo = UserRepository(db_session)

    user = repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd",
        role="gestion"
    )

    deleted = repo.delete_user(user.id)
    assert deleted is True

    user_check = repo.get_user_by_id(user.id)
    assert user_check is None


def test_delete_user_not_found(db_session):
    """Test de suppression d'un utilisateur qui n'existe pas"""
    repo = UserRepository(db_session)

    deleted = repo.delete_user(9999)
    assert deleted is False
