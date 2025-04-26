import sqlite3

def create_connection(db_file='app/storage/database.db'):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        create_database(conn)
        return conn
    except sqlite3.Error as e:
        print(e)

def create_database(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS family (
        id INTEGER PRIMARY KEY,
        type VARCHAR(255),
        date_of_entry DATE,
        thickness FLOAT,
        classification INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        role VARCHAR(255)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY,
        family_id INTEGER,
        date_of_fracture DATE,
        result BOOLEAN,
        operative INTEGER,
        FOREIGN KEY (family_id) REFERENCES family(id),
        FOREIGN KEY (operative) REFERENCES users(id)
    );
    """)

    conn.commit()

create_connection('app/storage/database.db')