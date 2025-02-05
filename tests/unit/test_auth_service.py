from services.auth_service import ph, set_password, verify_password  # noqa: F401, E501,  # type: ignore


def test_set_password():
    """
    Vérifie le hashage du pw avant stockage
    S'assure que le pw brut n'est pas récupérable à partir du hash
    """
    password = "password1234"
    hashed_password = set_password(password)

    assert hashed_password != password
    assert isinstance(hashed_password, str)
    assert ph.verify(hashed_password, password)


def test_verify_password_valid():
    """ Vérifie que le pw correspond au hash """
    password = "password1234"
    hashed_password = set_password(password)

    assert verify_password(hashed_password, password)


def test_verify_password_invalid():
    """ Vérifie la non-correspondance d'un pw avec un hash """
    password = "password1234"
    wrong_password = "wrongpassword1234"
    hashed_password = set_password(password)

    assert not verify_password(hashed_password, wrong_password)


def test_verify_password_exception():
    """ Vérifie la bonne gestion des erreurs en cas de hash invalides """
    malformed_hash = "malformedhash"

    assert not verify_password(malformed_hash, "anyPassword")


def test_set_password_multiple():
    """
    S'assure de la différence entre deux hash pour deux mots de passe
    identiques
    """
    password = "samePassword"
    hashed_password_1 = set_password(password)
    hashed_password_2 = set_password(password)

    assert hashed_password_1 != hashed_password_2
    assert verify_password(hashed_password_1, password)
    assert verify_password(hashed_password_2, password)
