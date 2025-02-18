import click

from commands.user import user_group


# Regroupement de toutes les commandes
@click.group()
def main():
    """CLI CRM Epic Events"""
    pass


# Ajout de sous-commandes sous chaque groupe
main.add_command(user_group)
# main.add_command(client_group)
# main.add_command(contract_group)
# main.add_command(event_group)

if __name__ == '__main__':
    main()
