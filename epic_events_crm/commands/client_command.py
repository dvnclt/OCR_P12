import click

from config.config import SessionLocal
from services.client_service import ClientService
from repositories.client_repository import ClientRepository
from commands.user_command import user_service

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
@click.option('--full_name', prompt="Nom complet du client",
              help="Nom complet du client.")
@click.option('--email', prompt="Email du client",
              help="Adresse email du client.")
@click.option('--phone', prompt="Numéro de téléphone du client",
              help="Numéro de téléphone du client.")
@click.option('--company_name', prompt="Nom de l'entreprise",
              help="Nom de l'entreprise du client.")
def create(ctx, full_name, email, phone, company_name):
    """Crée un nouveau client."""

    user = ctx.obj
    contact = user.full_name

    confirm = click.confirm(
        f"❗ Confirmez-vous la création du client ?\n"
        f"Nom complet : {full_name}\n"
        f"Email : {email}\n"
        f"Téléphone : {phone}\n"
        f"Entreprise : {company_name}\n"
        f"Contact : {contact}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    client = client_service.create_client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        contact=contact
    )

    if isinstance(client, dict) and "error" in client:
        click.echo(f"❌ Erreur : {client['error']}")
        raise click.Abort()

    click.echo(f"✅ Client {full_name} créé avec succès.")


# Commande pour récupérer un client par email
@client_group.command()
@click.option('--email', prompt="Email du client",
              help="Email du client à récupérer.")
def get(email):
    """Récupère un client par son email."""

    client = client_service.get_client_by_email(email)

    if isinstance(client, dict) and "error" in client:
        click.echo(f"❌ Erreur : {client['error']}")
    else:
        click.echo(
            f"👤 Client trouvé :\n"
            f"Nom :{client.full_name}\n"
            f"Email {client.email}\n"
            f"Téléphone : {client.phone}\n"
            f"Entreprise : {client.company_name}\n"
            f"Contact : {client.contact}"
        )


# Commande pour mettre à jour un client via son email
@client_group.command()
@click.option('--email', prompt="Email du client à modifier",
              help="Email du client.")
def update(email):
    """Met à jour les informations d'un client via son email."""

    # Récupère le client existant
    client = client_service.get_client_by_email(email)

    if client is None or (isinstance(client, dict) and "error" in client):
        click.echo("❌ Erreur : Client introuvable.")
        raise click.Abort()

    client_id = client.id

    # Demande les nouvelles valeurs avec les anciennes comme valeurs par défaut
    full_name = click.prompt("Nouveau nom complet (laisser vide pour ne "
                             "pas changer)",
                             default=client.full_name, show_default=True)
    email = click.prompt("Nouvelle adresse email (laisser vide pour ne "
                         "pas changer)",
                         default=client.email, show_default=True)
    phone = click.prompt("Nouveau téléphone (laisser vide pour ne pas "
                         "changer)",
                         default=client.phone, show_default=True)
    company_name = click.prompt("Nouvelle entreprise (laisser vide pour ne "
                                "pas changer)",
                                default=client.company_name, show_default=True)
    contact = click.prompt("Nouveau contact (laisser vide pour ne "
                           "pas changer)",
                           default=client.contact, show_default=True)

    if contact != client.contact:
        user_contact = user_service.get_user_by_name(contact)

        if user_contact is None or (isinstance(user_contact, dict) and "error"
                                    in user_contact):
            click.echo("❌ Erreur : Aucun utilisateur trouvé avec le nom "
                       f"'{contact}'.")
            raise click.Abort()

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
    client_to_delete = client_service.get_client_by_email(email)

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
