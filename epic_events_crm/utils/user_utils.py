import re


def is_email_valid(email):
    """Vérifie si une adresse email est valide."""
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None
