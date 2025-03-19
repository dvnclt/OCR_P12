import click
from datetime import datetime

from config.config import SessionLocal
from services.event_service import EventService
from repositories.event_repository import EventRepository
from commands.client_command import client_service
from commands.user_command import user_service
from commands.contract_command import contract_service
from utils.utils import is_date_valid


db_session = SessionLocal()
event_repo = EventRepository(db_session)
event_service = EventService(event_repo)


@click.group(name='event')
def event_group():
    """Groupe de commandes pour gérer les events"""
    pass


# Commande pour créer un contrat
@event_group.command()
def create():
    """Crée un nouvel event dans le CRM"""

    while True:
        contract_id = click.prompt("ID du contrat")
        contract = contract_service.get_contracts(contract_id)
        if contract is None or (isinstance(contract, dict) and "error" in
                                contract):
            click.echo(f"❌ Erreur : {contract['error']}")
        else:
            contract = contract[0]
            break
    name = click.prompt("Nom de l'évènement")

    while True:
        start_date = click.prompt("Date de début (YYYY-MM-DD)")
        if not is_date_valid(start_date):
            click.echo(f"❌ Erreur : Date invalide : {start_date} "
                       "Format attendu : YYYY-MM-DD")
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            break

    while True:
        start_date = click.prompt("Date de début (YYYY-MM-DD)")
        if not is_date_valid(start_date):
            click.echo(f"❌ Erreur : Date invalide : {start_date} "
                       "Format attendu : YYYY-MM-DD")
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            break

    end_date = click.prompt("Date de fin")
    location = click.prompt("Lieu")
    attendees = click.prompt("Nombre de participants", type=int)
    contact = click.prompt("Email du contact évènement")[0]
    notes = click.prompt("Notes")

    confirm = click.confirm(
        "\n❗ Confirmer la création de l'event ? :\n"
        f"Nom : {name}\n"
        f"Client : {contract.client.full_name}\n"
        f"  Adresse email : {contract.client.email}\n"
        f"  Téléphone : {contract.client.phone}\n"
        f"Date de début : {start_date}\n"
        f"Date de fin : {end_date}\n"
        f"Support Contact : {contact.full_name}\n"
        f"Lieu : {location}\n"
        f"Nombre de participants : {attendees}\n"
        f"Notes : {notes}\n"
        )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    # Création de l'event
    event = event_service.create_event(
        name=name,
        contract_id=contract.id,
        client_id=contract.client.id,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        contact=contact if contact else None,
        user_id=contact.id,
        notes=notes
    )

    if isinstance(event, dict) and "error" in event:
        click.echo(f"❌ Erreur : {event['error']}")
        return

    click.echo("✅ Evènement créé avec succès :\n"
               f"\nID : {event.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {event.contract.client.full_name}\n"
               f"   Email : {event.contract.client.email}\n"
               f"   Téléphone : {event.contract.client.phone}\n"
               f"\nDate de début : {event.start_date}"
               f"Date de fin : {event.end_date}"
               f"Contact : {event.contact}\n"
               f"Lieu : {event.location}\n"
               f"Nombre de participants : {event.attendees}\n"
               f"Notes : {event.notes}\n"
               )
