PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS families (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_place TEXT NOT NULL,
    type TEXT NOT NULL,
    date_of_entry DATE NOT NULL,
    radius FLOAT,
    height FLOAT,
    classification INTEGER,
    client_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fingerprint_id INTEGER NOT NULL,
    is_active INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    family_id INTEGER NOT NULL,
    date_of_fracture DATE NOT NULL,
    fractured_at DATE,
    result INTEGER,
    operative INTEGER,        
    is_reported INTEGER,
    fracture_days INTEGER,

    FOREIGN KEY (family_id) REFERENCES families(id),
    FOREIGN KEY (operative) REFERENCES users(id)
);
