-- Tabla: clients
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Tabla: projects
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    client_id INTEGER  -- Puede ser NULL
);

-- Tabla: users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    role TEXT,
    username TEXT UNIQUE,
    password TEXT,
    is_active INTEGER DEFAULT 1  -- 1 = activo, 0 = eliminado lógicamente
);

-- Tabla: families
CREATE TABLE IF NOT EXISTS families (
    id INTEGER PRIMARY KEY,
    type TEXT,
    date_of_entry TEXT,  -- Fecha como texto (YYYY-MM-DD)
    radius REAL,
    height REAL,
    classification INTEGER,
    client_id INTEGER,   -- Puede ser NULL
    project_id INTEGER,   -- Puede ser NULL
    design_resistance REAL
);

-- Tabla: samples
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    family_id INTEGER,   -- Puede ser NULL
    date_of_fracture TEXT,  -- Fecha como texto (YYYY-MM-DD)
    result INTEGER,
    operative INTEGER,   -- Puede ser NULL
    is_reported INTEGER  -- 1 = reportado, 0 = no reportado
);
