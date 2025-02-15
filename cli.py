import click

from epic_events_crm.services.user_service import UserService
from epic_events_crm.services.client_service import ClientService
from epic_events_crm.services.contract_service import ContractService
from epic_events_crm.services.event_service import EventService
from epic_events_crm.repositories.user_repository import UserRepository
from epic_events_crm.repositories.client_repository import ClientRepository
from epic_events_crm.repositories.contract_repository import ContractRepository
from epic_events_crm.repositories.event_repository import EventRepository

# Création des objets services
user_repo = UserRepository()
client_repo = ClientRepository()
contract_repo = ContractRepository()
event_repo = EventRepository()

user_service = UserService(user_repo)
client_service = ClientService(client_repo)
contract_service = ContractService(contract_repo)
event_service = EventService(event_repo)


@click.group()
def cli():
    """CRM CLI - Commandes pour gérer les clients, utilisateurs,  etc."""
    pass


# Commande pour créer un utilisateur (exemple basique)
@cli.command()
@click.option('--email', prompt='Email de l\'utilisateur',
              help='L\'email de l\'utilisateur.')
@click.option('--role', prompt='Rôle de l\'utilisateur',
              help='Le rôle de l\'utilisateur (admin, gestion, etc.).')
def create_user(email, role):
    """Crée un nouvel utilisateur dans le CRM."""
    result = user_service.create_user(email=email, role=role)
    click.echo(result)


if __name__ == '__main__':
    cli()
