import click

from config.config import SessionLocal
from repositories.user_repository import UserRepository
from services.user_service import UserService
from services.auth_service import set_token, get_token, clear_token
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
    if ctx.invoked_subcommand not in ["login", "logout"]:
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


# Ajout de sous-commandes sous chaque groupe
main.add_command(user_group)
main.add_command(client_group)
main.add_command(contract_group)
main.add_command(event_group)

if __name__ == '__main__':
    main()
