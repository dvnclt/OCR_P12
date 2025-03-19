import click

from config.config import SessionLocal
from services.client_service import ClientService
from repositories.client_repository import ClientRepository
from commands.user_command import user_service
from utils.utils import is_email_valid, is_phone_valid


db_session = SessionLocal()

# Création des objets services
client_repo = ClientRepository(db_session)
client_service = ClientService(client_repo)


@click.group(name='client')
def client_group():
    """Groupe de commandes pour gérer les clients."""
    pass


# Commande pour créer un client
@client_group.command()
@click.pass_context
def create(ctx):
    """Crée un nouveau client dans le CRM."""

    # Demande le nom complet
    full_name = click.prompt("Nom complet du client")

    # Demande et vérifie l'email
    while True:
        email = click.prompt("Email du client").lower()
        if not is_email_valid(email):
            click.echo(f"❌ Erreur : L'email '{email}' est invalide.")
        else:
            break

    # Demande et vérifie le numéro de téléphone
    while True:
        phone = click.prompt("Numéro de téléphone du client")
        if not is_phone_valid(phone):
            click.echo(f"❌ Erreur : Le numéro '{phone}' est invalide.")
        else:
            break

    # Demande le nom de l'entreprise
    company_name = click.prompt("Nom de l'entreprise")

    # Associe l'user qui créé le client comme étant don contact
    user = ctx.obj
    contact = user.full_name
    if not contact:
        click.echo("❌ Erreur : Contact introuvable")
        return

    # Confirmation avant création
    confirm = click.confirm(
        "\n❗ Confirmer la création du client ? :\n"
        f"Nom : {full_name}\n"
        f"Email : {email}\n"
        f"Téléphone : {phone}\n"
        f"Entreprise : {company_name}\n"
        f"Contact : {contact}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    # Création du client
    client = client_service.create_client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        contact=contact if contact else None
    )

    if isinstance(client, dict) and "error" in client:
        click.echo(f"❌ Erreur : {client['error']}")
        return

    click.echo(f"✅ Création du client {full_name} réussie.\n"
               f"Email : {email}\n"
               f"Téléphone : {phone}\n"
               f"Entreprise : {company_name}\n"
               f"Contact : {contact}\n"
               )


# Commande pour récupérer un client
@client_group.command()
@click.argument('identifier', nargs=-1, required=False)
def get(identifier):
    """Récupère un client par ID, email ou nom complet."""

    if identifier:
        identifier = " ".join(identifier)
    # Si aucun argument n'est passé, demande à l'utilisateur
    if not identifier:
        identifier = click.prompt(
            'Veuillez entrer un ID, un email ou un nom complet',
            type=str
        )

    # Récupération du client en fonction de l'identifiant
    if identifier.isdigit():
        found_client = client_service.get_client_by_id(int(identifier))
    elif "@" in identifier:
        found_client = client_service.get_client_by_email(identifier.lower())
    else:
        found_client = client_service.get_client_by_name(identifier)

    # Gestion des erreurs
    if isinstance(found_client, dict) and "error" in found_client:
        click.echo(f"❌ Erreur : {found_client['error']}")
        return

    # Si le client n'est pas trouvé
    if not found_client:
        click.echo("❌ Aucun client trouvé.")
    elif isinstance(found_client, list) and len(found_client) > 1:
        click.echo("✅ Plusieurs clients ont été trouvés :")
        for c in found_client:
            click.echo(
                f"\n👤 {c.full_name}\n"
                f"ID : {c.id}\n"
                f"Email : {c.email}\n"
                f"Téléphone : {c.phone}\n"
                f"Entreprise : {c.company_name}\n"
                f"Contact : {c.contact}\n"
            )
    else:
        c = found_client[0] if isinstance(found_client, list) else found_client
        click.echo("\n✅ Client trouvé :\n"
                   f"\n👤 {c.full_name}\n"
                   f"ID : {c.id}\n"
                   f"Email : {c.email}\n"
                   f"Téléphone : {c.phone}\n"
                   f"Entreprise : {c.company_name}\n"
                   f"Contact : {c.contact}\n"
                   )


# Commande pour mettre à jour un client via son email
@client_group.command()
@click.option('--email', prompt="Email du client à modifier",
              help="Email du client.")
def update(email):
    """Met à jour les informations d'un client via son email."""

    # Récupère le client existant
    client = client_service.get_client_by_email(email.lower())

    if client is None or (isinstance(client, dict) and "error" in client):
        click.echo("❌ Erreur : Client introuvable.")
        raise click.Abort()

    client_id = client.id

    click.echo("\n👤 Client trouvé :\n"
               f"Nom : {client.full_name}\n"
               f"Email : {client.email}\n"
               f"Téléphone : {client.phone}\n"
               f"Entreprise : {client.company_name}\n"
               f"Contact : {client.contact}\n"
               )

    # Demande les nouvelles valeurs avec les anciennes comme valeurs par défaut
    full_name = click.prompt("Nouveau nom complet (laisser vide pour ne "
                             "pas changer)",
                             default=client.full_name, show_default=True)

    while True:
        email = click.prompt("Nouvelle adresse email (laisser vide pour ne "
                             "pas changer)", default=client.email,
                             show_default=True).lower()
        if not is_email_valid(email):
            click.echo(f"❌ Erreur : L'email '{email}' est invalide.")
        else:
            break

    while True:
        phone = click.prompt("Nouveau téléphone (laisser vide pour ne pas "
                             "changer)", default=client.phone,
                             show_default=True)
        if not is_phone_valid(phone):
            click.echo(f"❌ Erreur : Le numéro '{phone}' est invalide.")
        else:
            break
    company_name = click.prompt("Nouvelle entreprise (laisser vide pour ne "
                                "pas changer)",
                                default=client.company_name, show_default=True)

    while True:
        contact = click.prompt("Nom du nouveau contact (laisser vide pour ne "
                               "pas changer)",
                               default=client.contact, show_default=True)
        if contact != client.contact:
            user_contact = user_service.get_user_by_name(contact)

            if user_contact is None or (isinstance(user_contact, dict) and
                                        "error" in user_contact):
                click.echo("❌ Erreur : Aucun utilisateur trouvé avec le nom "
                           f"'{contact}'.")
            else:
                break
        else:
            break

    # Si aucun changement, annule l'opération
    if (
        full_name == client.full_name
        and email == client.email
        and phone == client.phone
        and company_name == client.company_name
        and contact == client.contact
    ):
        click.echo("ℹ️ Aucune modification appliquée.")
        return

    confirm = click.confirm(
        f"❗ Valider les modifications suivantes ?\n"
        f"{client.full_name} => {full_name}\n"
        f"{client.email} => {email}\n"
        f"{client.phone} => {phone}\n"
        f"{client.company_name} => {company_name}\n"
        f"{client.contact} => {contact}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    # Applique la mise à jour
    updated_client = client_service.update_client(
        client_id=client_id,
        full_name=full_name if full_name != client.full_name else None,
        email=email if email != client.email else None,
        phone=phone if phone != client.phone else None,
        company_name=company_name if company_name != client.company_name
        else None,
        contact=contact if contact != client.contact else None
    )

    if isinstance(updated_client, dict) and "error" in updated_client:
        click.echo(f"❌ Erreur : {updated_client['error']}")
        raise click.Abort()

    click.echo(f"✅ Mise à jour réussie pour {updated_client.full_name}.")


# Commande pour supprimer un client par email
@client_group.command()
@click.option('--email', prompt="Email du client à supprimer",
              help="Email du client à supprimer.")
def delete(email):
    """Supprime un client par son email."""

    # Recherche du client par email
    client_to_delete = client_service.get_client_by_email(email.lower())

    if isinstance(client_to_delete, dict) and "error" in client_to_delete:
        click.echo(f"❌ Erreur : {client_to_delete['error']}")
        raise click.Abort()

    # Demande confirmation pour la suppression
    confirm = click.confirm(
        f"❗ Êtes-vous sûr de vouloir supprimer {client_to_delete.full_name} "
        f"({client_to_delete.email}) ?"
    )

    if not confirm:
        click.echo("ℹ️ Suppression annulée.")
        return

    # Suppression du client
    result = client_service.delete_client(client_to_delete.id)

    if isinstance(result, dict) and "error" in result:
        click.echo(f"❌ Erreur : {result['error']}")
    else:
        click.echo(f"✅ Le client {client_to_delete.full_name} a été supprimé.")
