-- Tabla: clients
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Tabla: projects
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client_id INTEGER NOT NULL
);

-- Tabla: families
CREATE TABLE IF NOT EXISTS families (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    date_of_entry DATE NOT NULL,
    radius FLOAT,
    height FLOAT,
    classification INTEGER,
    client_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL
);

-- Tabla: users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Tabla: members
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    family_id INTEGER NOT NULL,
    date_of_fracture DATE,     -- fecha programada para fracturar
    fractured_at DATE,         -- fecha real en que se fracturó
    result INTEGER,
    operative INTEGER,
    is_reported INTEGER
);
