import click
from config.config import SessionLocal
from services.contract_service import ContractService
from repositories.contract_repository import ContractRepository
from commands.client_command import client_service
from commands.user_command import user_service
from utils.utils import is_email_valid


db_session = SessionLocal()
contract_repo = ContractRepository(db_session)
contract_service = ContractService(contract_repo)


@click.group(name='contract')
def contract_group():
    """Groupe de commandes pour gérer les contrats."""
    pass


# Commande pour créer un contrat
@contract_group.command()
def create():
    """Crée un nouveau contrat dans le CRM."""

    # Demande l'email du client
    while True:
        client_email = click.prompt("Email du client").lower()
        if not is_email_valid(client_email):
            click.echo(f"❌ Erreur : L'email '{client_email}' est invalide.")
            continue

        client = client_service.get_client_by_email(client_email)
        # Vérifie si le client existe bien
        if client is None or (isinstance(client, dict) and "error" in client):
            click.echo("❌ Erreur : Aucun client trouvé avec l'adresse email "
                       f"'{client_email}'.")
        else:
            break

    # Demande le montant du contrat
    while True:
        total_amount = click.prompt("Montant du contrat", type=float)
        if total_amount <= 0:
            click.echo("❌ Erreur : Le montant du contrat doit être un nombre "
                       "positif.")
        else:
            break

    # Demande le statut du contrat
    status = click.prompt("Statut du contrat (laisser vide si non "
                          "signé)", default="Non Signé").lower()

    confirm = click.confirm(
        "\n❗ Confirmer la création du contrat ? :\n"
        f"\nClient : {client.full_name}\n"
        f"\nContact : {client.contact}\n"
        f"Montant total : {total_amount}\n"
        f"Statut : {status}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    # Création du contrat
    contract = contract_service.create_contract(
        client_id=client.id,
        total_amount=total_amount,
        status=status,
        contact=client.contact if client.contact else None
    )

    if isinstance(contract, dict) and "error" in contract:
        click.echo(f"❌ Erreur : {contract['error']}")
        return

    click.echo("✅ Contrat créé avec succès :\n"
               f"\nUUID : {contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {client.full_name}\n"
               f"   Email : {client.email}\n"
               f"   Téléphone : {client.phone}\n"
               f"   Entreprise : {client.company_name}\n"
               f"\nContact : {contract.contact}\n"
               f"Montant total : {contract.total_amount}\n"
               f"Montant payé : {contract.paid_amount}\n"
               f"Montant restant dû : {contract.remaining_amount}\n"
               f"Date de création : {contract.creation_date}\n"
               f"Statut : {contract.status}\n"
               )


@contract_group.command()
@click.argument("option", type=click.Choice(["all",
                                             "id",
                                             "user",
                                             "client",
                                             "remaining_amount",
                                             "status"
                                             ]))
def get(option):
    """Récupère les contrats liés à un utilisateur, un client, un statut..."""

    contracts = None

    if option == "all":
        contracts = contract_service.get_contracts()

    elif option == "id":
        contract_id = click.prompt("ID du contrat")
        contracts = contract_service.get_contracts(contract_id=contract_id)

    elif option == "user":
        user_email = click.prompt("Email de l'utilisateur").lower()
        user = user_service.get_user_by_email(user_email)
        contracts = contract_service.get_contracts(user_id=user.id)

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

        contracts = contract_service.get_contracts(client_id=client.id)

    elif option == "status":
        status = click.prompt("Statut des contrats à rechercher").lower()
        contracts = contract_service.get_contracts(status=status)

    elif option == "remaining_amount":
        contracts = contract_service.get_contracts(remaining_amount=True)

    # Vérification et affichage des contrats
    if not contracts:
        click.echo("❌ Aucun contrat trouvé.")
    elif isinstance(contracts, dict) and "error" in contracts:
        click.echo(f"❌ {contracts['error']}")
    else:
        for contract in contracts:
            click.echo(f"📄 UUID : {contract.id}\n"
                       f"\nInformations client :\n"
                       f"   Nom : {contract.client.full_name}\n"
                       f"   Email : {contract.client.email}\n"
                       f"   Téléphone : {contract.client.phone}\n"
                       f"   Entreprise : {contract.client.company_name}\n"
                       f"\nContact : {contract.contact}\n"
                       f"Montant total : {contract.total_amount}\n"
                       f"Montant payé : {contract.paid_amount}\n"
                       f"Montant restant dû : {contract.remaining_amount}\n"
                       f"Date de création : {contract.creation_date}\n"
                       f"Statut : {contract.status}\n"
                       )


# Commande pour mettre à jour un contrat
@contract_group.command()
@click.option('--contract_id', prompt="ID du contrat",
              help="ID du contrat à actualiser")
def update(contract_id):
    """Met à jour les informations d'un contrat."""

    # Récupère le contrat existant
    contract = contract_service.get_contracts(contract_id)
    if contract is None:
        click.echo("❌ Erreur : Contrat introuvable.")
        return

    contract = contract[0]

    click.echo("\n📄 Contrat trouvé :"
               f"UUID : {contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {contract.client.full_name}\n"
               f"   Email : {contract.client.email}\n"
               f"   Téléphone : {contract.client.phone}\n"
               f"   Entreprise : {contract.client.company_name}\n"
               f"\nContact : {contract.contact}\n"
               f"Montant total : {contract.total_amount}\n"
               f"Montant payé : {contract.paid_amount}\n"
               f"Montant restant dû : {contract.remaining_amount}\n"
               f"Date de création : {contract.creation_date}\n"
               f"Statut : {contract.status}\n"
               )

    # Demander les nouvelles valeurs
    contact = click.prompt("Email du nouveau contact "
                           "(laisser vide pour ne pas changer)",
                           default=contract.contact, show_default=True)
    total_amount = click.prompt("Nouveau montant total du contrat "
                                "(laisser vide pour ne pas changer)",
                                default=contract.total_amount,
                                show_default=True, type=float)

    status = click.prompt("Nouveau statut du contrat (laisser vide pour ne pas"
                          " changer)",
                          default=contract.status,
                          show_default=True)

    # Mettre à jour le contrat
    updated_contract = contract_service.update_contract(
        contract_id=contract_id,
        total_amount=total_amount if total_amount != contract.total_amount
        else None,
        status=status if status != contract.status else None,
        contact=contact if contact != contract.contact else None
    )

    click.echo("✅ Contrat mis à jour avec succès :\n"
               f"UUID : {updated_contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {updated_contract.client.full_name}\n"
               f"   Email : {updated_contract.client.email}\n"
               f"   Téléphone : {updated_contract.client.phone}\n"
               f"   Entreprise : {updated_contract.client.company_name}\n"
               f"\nContact : {updated_contract.contact}\n"
               f"Montant total : {updated_contract.total_amount}\n"
               f"Montant payé : {updated_contract.paid_amount}\n"
               f"Montant restant dû : {updated_contract.remaining_amount}\n"
               f"Date de création : {updated_contract.creation_date}\n"
               f"Statut : {updated_contract.status}\n"
               )


# Commande pour mettre à jour un contrat
@contract_group.command()
@click.option('--contract_id', prompt="ID du contrat",
              help="ID cu contrat à actualiser")
def payment(contract_id):
    """Met à jour le contrat en fonction du paiement"""

    # Récupère le contrat existant
    contract = contract_service.get_contracts(contract_id)
    if contract is None:
        click.echo("❌ Erreur : Contrat introuvable.")
        return

    contract = contract[0]

    click.echo("\n📄 Contrat trouvé :"
               f"UUID : {contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {contract.client.full_name}\n"
               f"   Email : {contract.client.email}\n"
               f"   Téléphone : {contract.client.phone}\n"
               f"   Entreprise : {contract.client.company_name}\n"
               f"\nContact : {contract.contact}\n"
               f"Montant total : {contract.total_amount}\n"
               f"Montant payé : {contract.paid_amount}\n"
               f"Montant restant dû : {contract.remaining_amount}\n"
               f"Date de création : {contract.creation_date}\n"
               f"Statut : {contract.status}\n"
               )

    # Demande le montant total du paiment
    amount = click.prompt("Montant du paiement (< ou = 0 : annulation)",
                          show_default=True, type=float)

    if amount <= 0:
        click.echo("ℹ️ Opération annulée.")
        return

    # Mettre à jour le contrat
    updated_contract = contract_service.update_contract(
        contract_id=contract_id,
        paid_amount=amount
        )

    click.echo("✅ Contrat mis à jour avec succès :\n"
               f"UUID : {updated_contract.id}\n"
               f"\nInformations client :\n"
               f"   Nom : {updated_contract.client.full_name}\n"
               f"   Email : {updated_contract.client.email}\n"
               f"   Téléphone : {updated_contract.client.phone}\n"
               f"   Entreprise : {updated_contract.client.company_name}\n"
               f"\nContact : {updated_contract.contact}\n"
               f"Montant total : {updated_contract.total_amount}\n"
               f"Montant payé : {updated_contract.paid_amount}\n"
               f"Montant restant dû : {updated_contract.remaining_amount}\n"
               f"Date de création : {updated_contract.creation_date}\n"
               f"Statut : {updated_contract.status}\n"
               )


# Commande pour supprimer un contrat
@contract_group.command()
@click.option('--contract_id', prompt="ID du contrat")
def delete(contract_id):
    """Supprime un contrat par son UUID."""

    contract_to_delete = contract_service.get_contracts(contract_id)[0]

    # Demande confirmation avant suppression
    confirm = click.confirm("\n❗ Êtes-vous sûr de vouloir supprimer le contrat"
                            " suivant ?\n"
                            f"\nUUID : {contract_to_delete.id}\n"
                            f"\nInformations client :\n"
                            f"   Nom : {contract_to_delete.client.full_name}\n"
                            f"   Email : {contract_to_delete.client.email}\n"
                            f"   Téléphone : {contract_to_delete.client.phone}\n"  # noqa: E501
                            f"   Entreprise : {contract_to_delete.client.company_name}\n"  # noqa: E501
                            f"\nContact : {contract_to_delete.contact}\n"
                            f"Montant total : {contract_to_delete.total_amount}\n"  # noqa: E501
                            f"Montant payé : {contract_to_delete.paid_amount}\n"  # noqa: E501
                            f"Montant restant dû : {contract_to_delete.remaining_amount}\n"  # noqa: E501
                            f"Date de création : {contract_to_delete.creation_date}\n"  # noqa: E501
                            f"Statut : {contract_to_delete.status}\n"
                            )
    if not confirm:
        click.echo("ℹ️ Suppression annulée.")
        return

    # Suppression du contrat
    result = contract_service.delete_contract(contract_to_delete.id)
    if isinstance(result, dict) and "error" in result:
        click.echo(f"❌ Erreur : {result['error']}")
    else:
        click.echo(f"✅ Le contrat ID {contract_to_delete.id} a été supprimé.")
