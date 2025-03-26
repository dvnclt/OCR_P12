import click

from config.config import SessionLocal
from repositories.user_repository import UserRepository
from services.user_service import UserService
from utils.auth_utils import set_token, get_token, clear_token, set_password
from utils.jwt_utils import get_current_user

from commands.user_command import user_group
from commands.client_command import client_group
from commands.contract_command import contract_group
from commands.event_command import event_group


db_session = SessionLocal()

# Création des objets services
user_repo = UserRepository(db_session)
user_service = UserService(user_repo)


# Regroupement de toutes les commandes
@click.group()
@click.pass_context
def main(ctx):
    """Vérification du token avant chaque commande excepté login/logout"""
    if ctx.invoked_subcommand not in ["login", "logout", "admin"]:
        token = get_token()
        user = get_current_user(token, user_repo)
        if isinstance(user, dict) and "error" in user:
            click.echo(f"❌ Erreur : {user['error']}")
            raise click.Abort()
        # Stocke l'utilisateur pour les commandes suivantes
        ctx.obj = user


# Commande pour authentifier un utilisateur
@main.command()
@click.option('--email', prompt='Email de l\'utilisateur',
              help='L\'email de l\'utilisateur.')
@click.option('--password', prompt='Mot de passe de l\'utilisateur',
              hide_input=True,
              help='Le mot de passe de l\'utilisateur.')
def login(email, password):
    """Authentifie l'utilisateur et génère un token JWT."""

    email = email.strip().lower()
    token = user_service.authenticate(email=email, password=password)

    if isinstance(token, dict) and "error" in token:
        click.echo(f"❌ Erreur : {token['error']}")
        raise click.Abort()

    clear_token()
    set_token(token)

    click.echo("✅ Authentification réussie.")


@main.command()
def logout():
    result = user_service.logout()
    click.echo("✅"+result["message"] if "message" in result
               else result["error"])


@main.command()
def admin():
    from models.user import User

    full_name = "admin"
    email = "admin"
    password = "admin"
    role_id = 1

    # Vérifie si l'admin existe déjà
    existing_admin = db_session.query(User).filter_by(role_id=role_id).first()
    if existing_admin:
        click.echo(f"❌ Erreur : {full_name} déjà existant")
        return

    # Création de l'admin en base
    admin_user = user_repo.create_user(
        full_name=full_name,
        email=email,
        hashed_password=set_password(password),
        role_id=role_id
    )

    click.echo(f"✅ Création de {admin_user.full_name} réussie.")


@main.command()
def sentry():
    division_by_zero = 1 / 0
    print(division_by_zero)


# Ajout de sous-commandes sous chaque groupe
main.add_command(user_group)
main.add_command(client_group)
main.add_command(contract_group)
main.add_command(event_group)

if __name__ == '__main__':
    main()
