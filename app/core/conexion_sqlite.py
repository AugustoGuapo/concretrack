import sqlite3

try:
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("""

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  role TEXT
);
""")

except sqlite3.Error as ex:
 
    print(ex)