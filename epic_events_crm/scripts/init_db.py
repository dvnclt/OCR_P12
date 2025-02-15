from models.role import Role, Permission


def initialize_roles_and_permissions(db_session):

    # Rôles
    admin_role = Role(name='admin')
    gestion_role = Role(name='gestion')
    commercial_role = Role(name='commercial')
    support_role = Role(name='support')

    db_session.add(admin_role)
    db_session.add(gestion_role)
    db_session.add(commercial_role)
    db_session.add(support_role)

    # Permissions
    create_user_permission = Permission(name='create_user')
    read_user_permission = Permission(name='read_user')
    update_user_permission = Permission(name='update_user')
    delete_user_permission = Permission(name='delete_user')

    create_client_permission = Permission(name='create_client')
    read_client_permission = Permission(name='read_client')
    update_client_permission = Permission(name='update_client')
    delete_client_permission = Permission(name='delete_client')

    create_contract_permission = Permission(name='create_contract')
    read_contract_permission = Permission(name='read_contract')
    update_contract_permission = Permission(name='update_contract')
    delete_contract_permission = Permission(name='delete_contract')

    create_event_permission = Permission(name='create_event')
    read_event_permission = Permission(name='read_event')
    update_event_permission = Permission(name='update_event')
    delete_event_permission = Permission(name='delete_event')

    db_session.add(create_user_permission)
    db_session.add(read_user_permission)
    db_session.add(update_user_permission)
    db_session.add(delete_user_permission)

    db_session.add(create_client_permission)
    db_session.add(read_client_permission)
    db_session.add(update_client_permission)
    db_session.add(delete_client_permission)

    db_session.add(create_contract_permission)
    db_session.add(read_contract_permission)
    db_session.add(update_contract_permission)
    db_session.add(delete_contract_permission)

    db_session.add(create_event_permission)
    db_session.add(read_event_permission)
    db_session.add(update_event_permission)
    db_session.add(delete_event_permission)

    # Lier les rôles aux permissions
    admin_role.permissions = [
        create_user_permission,
        create_client_permission,
        create_contract_permission,
        create_event_permission,

        read_user_permission,
        read_client_permission,
        read_contract_permission,
        read_event_permission,

        update_user_permission,
        update_client_permission,
        update_contract_permission,
        update_event_permission,

        delete_user_permission,
        delete_client_permission,
        delete_contract_permission,
        delete_event_permission,
    ]

    gestion_role.permissions = [
        create_user_permission,
        create_contract_permission,

        read_user_permission,
        read_client_permission,
        read_contract_permission,
        read_event_permission,

        update_user_permission,
        update_contract_permission,
        update_event_permission,

        delete_user_permission,
    ]

    commercial_role.permissions = [
        create_client_permission,

        read_client_permission,
        read_contract_permission,
        read_event_permission,
    ]

    support_role.permissions = [
        read_client_permission,
        read_contract_permission,
        read_event_permission,
    ]

    db_session.commit()
