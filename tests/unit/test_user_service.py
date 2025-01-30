import pytest
from unittest.mock import MagicMock

from epic_events_crm.services.user_service import UserService
from epic_events_crm.repositories.user_repository import UserRepository
from epic_events_crm.models.user import User


@pytest.fixture
def mock_user_repo():
    """Fixture pour simuler le repository User"""
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repo):
    """Fixture pour instancier UserService avec un repository mocké"""
    return UserService(user_repo=mock_user_repo)


def test_create_user_existing_email(user_service, mock_user_repo):
    # Teste le cas où un utilisateur existe déjà avec cet email
    mock_user_repo.get_user_by_email.return_value = User(
        email="test@example.com", full_name="Test User",
        hashed_password="hashedpassword"
        )

    email = "test@example.com"
    full_name = "New User"
    password = "password"

    result = user_service.create_user(email, full_name, password)

    # Vérifie qu'une erreur est retournée pour email déjà existant
    assert result == {"error": "Cet adresse email est déjà utilisée"}, 400
    mock_user_repo.get_user_by_email.assert_called_once_with(email)


def test_create_user_success(user_service, mock_user_repo):
    # Teste le cas où aucun utilisateur n'existe avec cet email
    mock_user_repo.get_user_by_email.return_value = None
    mock_user_repo.create_user.return_value = User(
        email="test@example.com", full_name="New User",
        hashed_password="hashedpassword"
        )

    email = "test@example.com"
    full_name = "New User"
    password = "password"

    result = user_service.create_user(email, full_name, password)

    # Vérifie que la méthode create_user du repository est appelée
    # Vérifie qu'un nouvel utilisateur est créé
    assert result.email == "test@example.com"
    assert result.full_name == "New User"
    assert result.hashed_password == "hashedpassword"
    mock_user_repo.get_user_by_email.assert_called_once_with(email)
    mock_user_repo.create_user.assert_called_once_with(email, full_name,
                                                       "hashedpassword")


def test_create_user_sql_error(user_service, mock_user_repo):
    # Simule une erreur SQL (exemple: problème de base de données)
    mock_user_repo.create_user.side_effect = Exception("Erreur interne")

    email = "test@example.com"
    full_name = "New User"
    password = "newpassword"

    result = user_service.create_user(email, full_name, password)

    # Vérifie que l'erreur est correctement gérée
    assert result == {"error": "Erreur interne"}, 500
    mock_user_repo.create_user.assert_called_once_with(email, full_name,
                                                       "hashedpassword")
