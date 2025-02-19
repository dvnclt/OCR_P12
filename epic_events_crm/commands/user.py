import click

from config.config import SessionLocal
from services.user_service import UserService
from repositories.user_repository import UserRepository


db_session = SessionLocal()

# Création des objets services
user_repo = UserRepository(db_session)
user_service = UserService(user_repo)


@click.group(name='user')
def user_group():
    pass


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

    confirm = click.confirm(
        f"❗ Êtes-vous sûr de vouloir créer l'utilisateur {full_name} ?\n"
        f"email : {email}\n"
        f"role : {role_id}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    user = user_service.create_user(
        full_name=full_name,
        email=email,
        password=password,
        role_id=role_id
        )

    if isinstance(user, dict) and "error" in user:
        click.echo(f"❌ Erreur : {user['error']}")
        raise click.Abort()

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
            f"👤 Utilisateur trouvé : {user.id} {user.full_name} {user.email} "
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
            f"👤 Utilisateur trouvé : {user.id} {user.full_name} {user.email} "
            f"{user.role.name}"
            )


# Commande pour récupérer un utilisateur par email
@user_group.command()
@click.option('--email', prompt='Email de l\'utilisateur',
              help='Email de l\'utilisateur à récupérer.')
def get_by_email(email):
    """Récupère un utilisateur par son email."""

    user = user_service.get_user_by_email(email)

    if isinstance(user, dict) and "error" in user:
        click.echo(f"❌ Erreur : {user['error']}")
    else:
        click.echo(
            f"👤 Utilisateur trouvé : {user.id} {user.full_name} {user.email} "
            f"{user.role.name}"
            )


# Commande pour mettre à jour un utilisateur via son email
@user_group.command()
@click.option('--email', prompt="Email de l'utilisateur à modifier",
              help="Email de l'utilisateur.")
def update(email):
    """Met à jour les informations d'un utilisateur via son email"""

    # Récupère l'utilisateur si existant
    user = user_service.get_user_by_email(email)

    if user is None or (isinstance(user, dict) and "error" in user):
        click.echo("❌ Erreur : Utilisateur introuvable.")
        raise click.Abort()

    click.echo(f"👤 Utilisateur trouvé : {user.full_name} - {user.email} - "
               f"{user.role.name}")

    # Demande les nouvelles valeurs avec les anciennes comme valeurs par défaut
    full_name = click.prompt("Nouveau nom complet (laisser vide pour ne pas "
                             "changer)",
                             default=user.full_name, show_default=True)
    new_email = click.prompt("Nouvelle adresse email (laisser vide pour ne pas"
                             " changer)", default=user.email,
                             show_default=True)
    password = click.prompt("Nouveau mot de passe (laisser vide pour ne pas "
                            "changer)", default="", hide_input=True)
    role_id = click.prompt("Nouvel ID de rôle (laisser vide pour ne pas "
                           "changer)", default=user.role.id, show_default=True)

    # Si aucun changement, annule l'opération
    if (
        full_name == user.full_name
        and new_email == user.email
        and not password
        and int(role_id) == user.role.id
    ):
        click.echo("ℹ️ Aucune modification n'a été appliquée")
        return

    confirm = click.confirm(
        f"❗ Valider les modifications suivantes ?\n"
        f"{user.full_name} => {full_name}\n"
        f"{user.email} => {new_email}\n"
        f"Mot de passe\n"
        f"{user.role_id} => {role_id}\n"
    )

    if not confirm:
        click.echo("ℹ️ Opération annulée.")
        return

    # Applique la mise à jour
    updated_user = user_service.update_user(
        email=email,
        full_name=full_name if full_name != user.full_name else None,
        new_email=new_email if new_email != user.email else None,
        password=password if password else None,
        role_id=int(role_id) if int(role_id) != user.role.id else None
    )

    if isinstance(updated_user, dict) and "error" in updated_user:
        click.echo(f"❌ Erreur : {updated_user['error']}")
        raise click.Abort()

    click.echo(f"✅ Mise à jour réussie pour {updated_user.full_name}.")


@user_group.command()
@click.option('--email', prompt="Email de l'utilisateur à supprimer",
              help="Email de l'utilisateur à supprimer.")
def delete(email):
    """Supprime un utilisateur par son email."""

    # Recherche de l'utilisateur par email
    user_to_delete = user_service.get_user_by_email(email)

    if isinstance(user_to_delete, dict) and "error" in user_to_delete:
        click.echo(f"❌ Erreur : {user_to_delete['error']}")
        raise click.Abort()

    # Demande confirmation pour la suppression
    confirm = click.confirm(
        f"❗ Êtes-vous sûr de vouloir supprimer {user_to_delete.full_name} "
        f"({user_to_delete.email}) ?"
    )

    if not confirm:
        click.echo("ℹ️ Suppression annulée.")
        return

    # Suppression de l'utilisateur
    result = user_service.delete_user(user_to_delete.id)

    if isinstance(result, dict) and "error" in result:
        click.echo(f"❌ Erreur : {result['error']}")
    else:
        click.echo(f"✅ L'utilisateur {user_to_delete.full_name} a été "
                   "supprimé.")
