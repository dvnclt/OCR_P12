from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError

from services.user_service import UserService  # noqa: F401, E501,  # type: ignore
from services.auth_service import verify_password, set_password  # noqa: F401, E501,  # type: ignore
from repositories.user_repository import UserRepository  # noqa: F401, E501,  # type: ignore


def test_create_user_success(db_session):
    """Test de la création réussie d'un utilisateur via UserService"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    email = "test@example.com"
    full_name = "Test User"
    password = "hashedpwd"

    new_user = service.create_user(email, full_name, password)

    assert new_user is not None
    assert new_user.email == email
    assert new_user.full_name == full_name


def test_create_user_email_already_exists(db_session):
    """Test d'échec de la création d'un utilisateur si email existant"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    email = "duplicate@example.com"
    user_repo.create_user(email, "Existing User", "hashedpwd")

    response, status_code = service.create_user(email, "New User",
                                                "newpassword")

    assert status_code == 400
    assert response == {"error": "Cet adresse email est déjà utilisée"}


def test_create_user_sqlalchemy_error(db_session):
    """Test de la gestion d'une exception SQLAlchemyError"""
    # Créé un faux UserRepository
    user_repo = MagicMock()
    # Force get_user_by_email à lever une exception
    user_repo.get_user_by_email.side_effect = SQLAlchemyError("DB Error")
    # Injecte le faux repo dans UserService
    service = UserService(user_repo)

    # get_user_by_email levant une erreur, except SQLAlchemyError est exécuté
    response, status_code = service.create_user(
        "error@example.com",
        "Error User",
        "password"
        )

    assert status_code == 500
    assert response == {"error": "Erreur interne"}


def test_get_user_by_id_success(db_session):
    """Test de la récupération d'un utilisateur avec un ID valide"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    user = user_repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd"
    )

    retrieved_user = service.get_user_by_id(user.id)

    assert retrieved_user.id == user.id
    assert retrieved_user.email == user.email
    assert retrieved_user.full_name == user.full_name


def test_get_user_by_id_user_not_found(db_session):
    """Test de la gestion d'un utilisateur introuvable"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    response, status_code = service.get_user_by_id(9999)

    assert status_code == 404
    assert response == {"error": "Utilisateur introuvable"}


def test_get_user_by_id_sqlalchemy_error(db_session):
    """Test de la gestion d'une exception SQLAlchemyError"""
    user_repo = MagicMock()
    user_repo.get_user_by_id.side_effect = SQLAlchemyError("DB Error")
    service = UserService(user_repo)

    response, status_code = service.get_user_by_id(1)

    assert status_code == 500
    assert response == {"error": "Erreur interne du serveur"}


def test_get_user_by_email_success(db_session):
    """Test de la récupération d'un utilisateur par email existant"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    user = user_repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd"
    )

    retrieved_user = service.get_user_by_email(user.email)

    assert retrieved_user.email == user.email
    assert retrieved_user.full_name == user.full_name


def test_get_user_by_email_user_not_found(db_session):
    """Test de la gestion d'un utilisateur introuvable par email"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    response, status_code = service.get_user_by_email(
        "nonexistant@example.com")

    assert status_code == 404
    assert response == {"error": "Utilisateur introuvable"}


def test_get_user_by_email_sqlalchemy_error(db_session):
    """Test de la gestion d'une exception SQLAlchemyError"""
    user_repo = MagicMock()
    user_repo.get_user_by_email.side_effect = SQLAlchemyError("DB Error")
    service = UserService(user_repo)

    response, status_code = service.get_user_by_email("error@example.com")

    assert status_code == 500
    assert response == {"error": "Erreur interne du serveur"}


def test_update_user_success(db_session):
    """Test de mise à jour réussie d'un utilisateur"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    user = user_repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd"
        )

    updated_user = service.update_user(
        user.id,
        full_name="Updated User",
        email="updated@example.com",
        password="newpassword"
        )

    assert updated_user.full_name == "Updated User"
    assert updated_user.email == "updated@example.com"


def test_update_user_user_not_found(db_session):
    """Test de mise à jour d'un utilisateur avec un ID introuvable"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    response, status_code = service.update_user(
        9999,
        full_name="Nonexistent User",
        email="nonexistent@example.com",
        password="hashedpwd"
        )

    assert status_code == 404
    assert response == {"error": "Utilisateur introuvable"}


def test_update_user_password_hashing(db_session):
    """Test de la mise à jour du mot de passe avec hachage"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    user = user_repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd"
    )

    old_hashed_password = user.hashed_password
    updated_user = service.update_user(user.id, password="newpassword")

    assert updated_user.hashed_password != "newpassword"
    assert updated_user.hashed_password != old_hashed_password
    assert verify_password(updated_user.hashed_password, "newpassword")


def test_update_user_sqlalchemy_error(db_session):
    """Test de la gestion d'une exception SQLAlchemyError"""
    user_repo = MagicMock()
    user_repo.update_user.side_effect = SQLAlchemyError("DB Error")
    service = UserService(user_repo)

    response, status_code = service.update_user(
        1,
        full_name="Error User",
        email="error@example.com",
        password="hashedpwd"
        )

    assert status_code == 500
    assert response == {"error": "Erreur interne"}


def test_delete_user_success(db_session):
    """Test de la suppression réussie d'un utilisateur"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    user = user_repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd"
    )

    response, status_code = service.delete_user(user.id)

    assert status_code == 200
    assert response == {"message": "Utilisateur supprimé"}


def test_delete_user_not_found(db_session):
    """Test de suppression d'un utilisateur avec un ID introuvable"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    response, status_code = service.delete_user(9999)

    assert status_code == 404
    assert response == {"error": "Utilisateur introuvable"}


def test_delete_user_sqlalchemy_error(db_session):
    """Test de la gestion d'une exception SQLAlchemyError"""
    user_repo = MagicMock()
    user_repo.get_user_by_id.return_value = MagicMock(
        id=1,
        email="test@example.com",
        full_name="Test User"
        )

    user_repo.delete_user.side_effect = SQLAlchemyError("DB Error")
    service = UserService(user_repo)

    response, status_code = service.delete_user(1)

    assert status_code == 500
    assert response == {"error": "Erreur interne"}


def test_authenticate_success(db_session):
    """Test de l'authentification réussie de l'utilisateur"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    email = "test@example.com"
    full_name = "Test User"
    password = "password123"
    user = user_repo.create_user(
        email=email,
        full_name=full_name,
        hashed_password=set_password(password)
    )

    authenticated_user = service.authenticate(email, password)

    assert authenticated_user.id == user.id
    assert authenticated_user.email == user.email
    assert authenticated_user.full_name == user.full_name


def test_authenticate_user_not_found(db_session):
    """Test de l'échec d'authentification pour un utilisateur introuvable"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    response, status_code = service.authenticate(
        "nonexistent@example.com",
        "password123"
        )

    assert status_code == 404
    assert response == {"error": "Utilisateur introuvable"}


def test_authenticate_wrong_password(db_session):
    """Test de l'échec d'authentification pour un mot de passe incorrect"""
    user_repo = UserRepository(db_session)
    service = UserService(user_repo)

    email = "test@example.com"
    full_name = "Test User"
    password = "password123"
    user = user_repo.create_user(  # noqa: F841
        email=email,
        full_name=full_name,
        hashed_password=set_password(password)
    )

    response, status_code = service.authenticate(email, "wrongpassword")

    assert status_code == 401
    assert response == {"error": "Mot de passe incorrect"}


def test_authenticate_sqlalchemy_error(db_session):
    """Test de la gestion d'une exception SQLAlchemyError"""
    user_repo = MagicMock()
    user_repo.get_user_by_email.side_effect = SQLAlchemyError("DB Error")
    service = UserService(user_repo)

    response, status_code = service.authenticate(
        "test@example.com",
        "password123"
        )

    assert status_code == 500
    assert response == {"error": "Erreur interne du serveur"}
