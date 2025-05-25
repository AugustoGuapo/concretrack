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
    CREATE IF NOT EXISTS TABLE "users" (
        "id"	INTEGER,
        "first_name"	VARCHAR(255),
        "last_name"	VARCHAR(255),
        "role"	VARCHAR(255),
        "username"	TEXT,
        "password"	TEXT, fingerprint_id INTEGER,
        PRIMARY KEY("id")
    );

    CREATE UNIQUE INDEX users_fingerprint_id_IDX ON users (fingerprint_id);
    CREATE UNIQUE INDEX users_username_IDX ON users (username);
    CREATE UNIQUE INDEX users_id_IDX ON users (id);
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
