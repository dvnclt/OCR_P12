import click
from datetime import datetime

from config.config import SessionLocal
from services.event_service import EventService
from repositories.event_repository import EventRepository
from commands.client_command import client_service
from commands.user_command import user_service, user_repo
from commands.contract_command import contract_service
from utils.cli_utils import is_date_valid, is_email_valid


db_session = SessionLocal()
event_repo = EventRepository(db_session)
event_service = EventService(event_repo, user_repo)


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
        end_date = click.prompt("Date de fin (YYYY-MM-DD)")
        if not is_date_valid(end_date):
            click.echo(f"❌ Erreur : Date invalide : {end_date} "
                       "Format attendu : YYYY-MM-DD")
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            break

    location = click.prompt("Lieu")
    attendees = click.prompt("Nombre de participants", type=int)

    while True:
        contact_email = click.prompt("Email du contact évènement")
        contact = user_service.get_user_by_email(contact_email)
        if contact is None or (isinstance(contact, dict) and "error" in
                               contact):
            click.echo(f"❌ Erreur : {contact['error']}")
        else:
            break

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
        contact=contact.full_name if contact else None,
        user_id=contact.id,
        notes=notes
    )

    if isinstance(event, dict) and "error" in event:
        click.echo(f"❌ Erreur : {event['error']}")
        return

    click.echo("✅ Evènement créé avec succès :\n"
               f"\nID : {event.id}\n"
               f"Nom de l'évènement : {event.name}\n"
               f"ID du contrat : {event.contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {event.contract.client.full_name}\n"
               f"   Email : {event.contract.client.email}\n"
               f"   Téléphone : {event.contract.client.phone}\n"
               f"\nDate de début : {event.start_date}\n"
               f"Date de fin : {event.end_date}"
               f"Contact : {event.contact}\n"
               f"Lieu : {event.location}\n"
               f"Nombre de participants : {event.attendees}\n"
               f"Notes : {event.notes}\n"
               )


# Commande pour lire un contrat
@event_group.command()
@click.argument("option", type=click.Choice(["all",
                                             "id",
                                             "contract",
                                             "user",
                                             "client",
                                             "start_date",
                                             "end_date",
                                             "no_user"
                                             ]))
def get(option):
    """Récupère un event dans le CRM"""

    events = None

    if option == "all":
        events = event_service.get_events()

    elif option == "id":
        event_id = click.prompt("ID de l'évènement")
        events = event_service.get_events(event_id=event_id)

    elif option == "contract":
        contract_id = click.prompt("ID du contrat")
        events = event_service.get_events(contract_id=contract_id)

    elif option == "user":
        user_email = click.prompt("Adresse email du contact").lower()
        user = user_service.get_user_by_email(user_email)
        events = event_service.get_events(user_id=user.id)

    elif option == "client":
        while True:
            client_email = click.prompt("Email du client").lower()
            if not is_email_valid(client_email):
                click.echo(f"❌ Erreur : L'email '{client_email}' est invalide")
            else:
                break
        client = client_service.get_client_by_email(client_email)
        if not client:
            click.echo("❌ Erreur : Aucun client trouvé avec l'email "
                       f"{client_email}")
            return
        events = event_service.get_events(client_id=client.id)

    elif option == "start_date":
        start_date = click.prompt("Date de début de l'évènement")
        events = event_service.get_events(start_date=start_date)

    elif option == "end_date":
        end_date = click.prompt("Date de fin de l'évènement")
        events = event_service.get_events(end_date=end_date)

    elif option == "no_user":
        events = event_service.get_events(no_user=True)

    # Vérification et affichage des contrats
    if not events:
        click.echo("❌ Aucun évènement trouvé.")
    elif isinstance(events, dict) and "error" in events:
        click.echo(f"❌ {events['error']}")
    else:
        for event in events:
            click.echo(f"\nID : {event.id}\n"
                       f"Nom de l'évènement : {event.name}\n"
                       f"ID du contrat : {event.contract.id}\n"
                       f"\nInformations client :\n"
                       f"   Nom : {event.contract.client.full_name}\n"
                       f"   Email : {event.contract.client.email}\n"
                       f"   Téléphone : {event.contract.client.phone}\n"
                       f"\nDate de début : {event.start_date}\n"
                       f"Date de fin : {event.end_date}\n"
                       f"Contact : {event.contact if event.contact else None}\n"  # noqa: E501
                       f"Lieu : {event.location}\n"
                       f"Nombre de participants : {event.attendees}\n"
                       f"Notes : {event.notes}\n"
                       )


# Commande pour mettre à jour un évènement
@event_group.command()
@click.option('--event_id', prompt="ID de l'évènement",
              help="ID de l'évènement à actualiser")
def update(event_id):
    """Met à jour les informations d'un évènement"""

    event = event_service.get_events(event_id)
    if isinstance(event, list) and event:
        event = event[0]
    if event is None:
        click.echo("❌ Erreur : Evènement introuvable")
        return

    click.echo(f"\nEvènement trouvé\n"
               f"ID : {event.id}\n"
               f"Nom de l'évènement : {event.name}\n"
               f"ID du contrat : {event.contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {event.contract.client.full_name}\n"
               f"   Email : {event.contract.client.email}\n"
               f"   Téléphone : {event.contract.client.phone}\n"
               f"\nDate de début : {event.start_date}\n"
               f"Date de fin : {event.end_date}\n"
               f"Contact : {event.contact if event.contact else None}\n"  # noqa: E501
               f"Lieu : {event.location}\n"
               f"Nombre de participants : {event.attendees}\n"
               f"Notes : {event.notes}\n"
               )

    # Demander les nouvelles valeurs
    name = click.prompt("Nouveau nom (laisser vide pour ne pas changer)",
                        default=event.name, show_default=True)

    while True:
        start_date = click.prompt("Nouvelle date de début (YYYY-MM-DD)"
                                  "(laisser vide pour ne pas changer)",
                                  default=event.start_date, show_default=True)
        if not is_date_valid(start_date):
            click.echo(f"❌ Erreur : Date invalide : {start_date} "
                       "Format attendu : YYYY-MM-DD")
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            break

    while True:
        end_date = click.prompt("Nouvelle date de fin (YYYY-MM-DD)"
                                "(laisser vide pour ne pas changer)",
                                default=event.end_date, show_default=True)
        if not is_date_valid(end_date):
            click.echo(f"❌ Erreur : Date invalide : {end_date} "
                       "Format attendu : YYYY-MM-DD")
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            break

    while True:
        contact_obj = (user_service.get_user_by_name(event.contact)[0]
                       if event.contact else None)
        contact_email = click.prompt(
            "Email du nouveau contact (laisser vide pour ne pas changer)",
            default=contact_obj.email if contact_obj else "",
            show_default=True
        )

        if not is_email_valid(contact_email):
            click.echo(f"❌ Erreur : L'email '{contact_email}' est invalide")
            continue

        contact = user_service.get_user_by_email(contact_email)

        if isinstance(contact, dict) and "error" in contact:
            click.echo(f"❌ Erreur : {contact['error']}")
        else:
            break

    location = click.prompt("Nouveau lieu (laisser vide pour ne pas changer)",
                            default=event.location, show_default=True)
    attendees = click.prompt("Nombre de participants (laisser vide pour ne pas"
                             " changer", default=event.attendees,
                             show_default=True)
    notes = click.prompt("Nouvelle note (laisser vide pour ne pas changer)",
                         default=event.notes, show_default=True)

    # Si aucun changement, annule l'opération
    if (
        name == event.name
        and start_date == event.start_date
        and end_date == event.end_date
        and contact.full_name == event.contact
        and location == event.location
        and attendees == event.attendees
        and notes == event.notes
    ):
        click.echo("ℹ️ Aucune modification appliquée.")
        return

    confirm = click.confirm(
        f"❗ Valider les modifications suivantes ?\n"
        f"{event.name} => {name}\n"
        f"{event.start_date} => {start_date}\n"
        f"{event.end_date} => {end_date}\n"
        f"{event.contact if event.contact else None} => {contact.full_name}\n"
        f"{event.location} => {location}\n"
        f"{event.attendees} => {attendees}\n"
        f"{event.notes} => {notes}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    # ✅ Mise à jour de l'évènement
    updated_event = event_service.update_event(
        event_id=event_id,
        name=name if name != event.name else None,
        start_date=start_date if start_date != event.start_date else None,
        end_date=end_date if end_date != event.end_date else None,
        contact=contact.full_name if contact and contact != event.contact else None,  # noqa: E501
        user_id=contact.id if contact and contact != event.contact else None,  # noqa: E501
        location=location if location != event.location else None,
        attendees=attendees if attendees != event.attendees else None,
        notes=notes if notes != event.notes else None
    )
    print(f"DEBUG - Événement mis à jour : {updated_event}"
          f"(type: {type(updated_event)})")

    click.echo(f"\nEvènement mis à jour\n"
               f"ID : {updated_event.id}\n"
               f"Nom de l'évènement : {updated_event.name}\n"
               f"ID du contrat : {updated_event.contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {updated_event.contract.client.full_name}\n"
               f"   Email : {updated_event.contract.client.email}\n"
               f"   Téléphone : {updated_event.contract.client.phone}\n"
               f"\nDate de début : {updated_event.start_date}\n"
               f"Date de fin : {updated_event.end_date}\n"
               f"Contact : {updated_event.contact if updated_event.contact else None}\n"  # noqa: E501
               f"Lieu : {updated_event.location}\n"
               f"Nombre de participants : {updated_event.attendees}\n"
               f"Notes : {updated_event.notes}\n"
               )

    if isinstance(updated_event, dict) and "error" in updated_event:
        click.echo(f"❌ Erreur : {updated_event['error']}")
        raise click.Abort()

    click.echo(f"✅ Mise à jour réussie pour l'évènement {updated_event.name}.")
