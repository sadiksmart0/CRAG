import cassio


def create_keyspace(keyspace: str, session):

    keyspace_creation_query = f"""
    CREATE KEYSPACE IF NOT EXISTS {keyspace}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 3}};
    """
    
    # Verify the keyspace exists
    rows = session.execute(f"SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name = '{keyspace}';")
    if not rows:
        print("Keyspace not found!....creating...")
        # Create a keyspace
        session.execute(keyspace_creation_query)
        # Verify keyspace creation
        session.set_keyspace(keyspace)
        print(f"Keyspace {keyspace} has been created and set.")
        cassio.init(session=session, keyspace=keyspace)
        return 0
    else:
        print(f"\n\nTHE KEYSPACE {keyspace} ALREADY EXIST.")
        cassio.init(session=session, keyspace=keyspace)
        return 1
