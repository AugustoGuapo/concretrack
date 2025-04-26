from app.storage import db_connection

def search_all_users():
    conn = db_connection.create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_all_families():
    conn = db_connection.create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM family")
    rows = cursor.fetchall()
    conn.close()
    return rows