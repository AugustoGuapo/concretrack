import sqlite3


def create_connection(db_file='app/storage/concretrack.db')-> sqlite3.Connection:
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        create_database(conn)
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Error connecting to database: {e}")


def create_database(conn):
    cursor = conn.cursor()
    with open('app/storage/schema.sql', 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
