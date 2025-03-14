import re


def is_role_valid(role_name):
    # Mapping des rôles
    ROLE_MAPPING = {
        "gestion": 2,
        "commercial": 3,
        "support": 4
    }
    return ROLE_MAPPING.get(role_name)


def is_email_valid(email):
    """Vérifie si une adresse email est valide."""
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None


def is_phone_valid(phone: str) -> bool:
    """
    Vérifie le format d'un numéro de téléphone
    Formats acceptés :
      - "+33 X 12 34 56 78"
      - "0X12345678"
      - "0X-12-34-56-78"
      - "0X 23 45 67 89"
    """
    pattern = r"^(?:\+33|0)[1-9](?:[\s.-]?\d{2}){4}$"
    return bool(re.match(pattern, phone))


def is_password_valid(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
