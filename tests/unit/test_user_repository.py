from repositories.user_repository import UserRepository  # noqa: F401, E501,  # type: ignore


def test_create_user(db_session):
    """Test de création d'un utilisateur"""
    repo = UserRepository(db_session)

    new_user = repo.create_user(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashedpwd"
        )

    assert new_user is not None
    assert new_user.full_name == "Test User"
    assert new_user.email == "test@example.com"
