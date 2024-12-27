from sqlmodel import Field, SQLModel, create_engine
from typing import Optional, List

def construct_postgresql_connection_string(host, port, database, username=None, password=None):
    """
    Constructs a PostgreSQL connection string for SQLAlchemy.

    Args:
        host (str): The hostname or IP address of the database server.
        port (int): The port number for the database server.
        database (str): The name of the database to connect to.
        username (str, optional): The username for the database. Default is None.
        password (str, optional): The password for the database. Default is None.

    Returns:
        str: A PostgreSQL connection string for use with SQLAlchemy's create_engine.
    """
    # Base connection string
    connection_string = f"postgresql+psycopg2://"

    # Include username and password if provided
    if username and password:
        connection_string += f"{username}:{password}@"

    # Add host, port, and database
    connection_string += f"{host}:{port}/{database}"

    return connection_string

# # Example usage
# host = "localhost"
# port = 5432
# database = "mydatabase"
# username = None  # or ""
# password = None  # or ""

# connection_string = construct_postgresql_connection_string(host, port, database, username, password)

# # Use with create_engine
# engine = create_engine(connection_string)


def sync_loras_records(loc_records: List[str]):
    return