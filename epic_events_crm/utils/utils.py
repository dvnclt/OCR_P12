import re


# Mapping des rôles
ROLE_MAPPING = {
    "gestion": 2,
    "commercial": 3,
    "support": 4
}


def is_email_valid(email):
    """Vérifie si une adresse email est valide."""
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None


def is_password_valid(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
