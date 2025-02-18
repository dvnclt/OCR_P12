import click

from config.config import SessionLocal
from services.auth_service import set_token, clear_token

from services.user_service import UserService
from repositories.user_repository import UserRepository


db_session = SessionLocal()

# Création des objets services
user_repo = UserRepository(db_session)
user_service = UserService(user_repo)


@click.group(name='user')
def user_group():
    """CLI CRM Epic Events - Gestion des utilisateurs"""
    pass


# Commande pour authentifier un utilisateur
@user_group.command()
@click.option('--email', prompt='Email de l\'utilisateur',
              help='L\'email de l\'utilisateur.')
@click.option('--password', prompt='Mot de passe de l\'utilisateur',
              help='Le mot de passe de l\'utilisateur.')
def login(email, password):
    """Authentifie l'utilisateur et génère un token JWT."""

    token = user_service.authenticate(email=email, password=password)
    if not token:
        raise click.Abort()
    clear_token()
    set_token(token)

    click.echo("✅ Authentification réussie.")


# Commande pour créer un utilisateur
@user_group.command()
@click.option('--full_name', prompt='Nom complet de l\'utilisateur',
              help='Nom complet de l\'utilisateur.')
@click.option('--email', prompt='Email de l\'utilisateur',
              help='L\'email de l\'utilisateur.')
@click.option('--password', prompt='Mot de passe de l\'utilisateur',
              help='Mot de passe de l\'utilisateur.', hide_input=True)
@click.option('--role_id', prompt='ID du rôle de l\'utilisateur',
              help='ID du rôle de utilisateur (2 = gestion, 3 = commercial, 4 = support).')  # noqa =: E501
def create(full_name, email, password, role_id):
    """Crée un nouvel utilisateur dans le CRM."""

    user_service.create_user(
        full_name=full_name,
        email=email,
        password=password,
        role_id=role_id
        )

    click.echo(f"✅ Création de l'utilisateur {full_name} réussie.")


# Commande pour récupérer un utilisateur par ID
@user_group.command()
@click.option('--user_id', prompt='ID de l\'utilisateur',
              help='ID de l\'utilisateur à récupérer.', type=int)
def get_by_id(user_id):
    """Récupère un utilisateur par son ID."""

    user = user_service.get_user_by_id(user_id)

    if isinstance(user, dict) and "error" in user:
        click.echo(f"❌ Erreur : {user['error']}")
    else:
        click.echo(
            f"👤 Utilisateur trouvé : {user.full_name} {user.email} "
            f"{user.role.name}"
            )


# Commande pour récupérer un utilisateur par son nom complet
@user_group.command()
@click.option('--full_name', prompt='Nom complet de l\'utilisateur',
              help='Nom complet de l\'utilisateur à récupérer.')
def get_by_name(full_name):
    """Récupère un utilisateur par son nom complet."""

    user = user_service.get_user_by_name(full_name)

    if isinstance(user, dict) and "error" in user:
        click.echo(f"❌ Erreur : {user['error']}")
    else:
        click.echo(
            f"👤 Utilisateur trouvé : {user.full_name} {user.email} "
            f"{user.role.name}"
            )
