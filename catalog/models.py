import sqlite3

CATALOG_DB = "catalog.db"

def init_catalog():
    conn = sqlite3.connect(CATALOG_DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    source TEXT,
                    schema TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transformations (
                    id INTEGER PRIMARY KEY,
                    dataset_id INTEGER,
                    step_name TEXT,
                    description TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(dataset_id) REFERENCES datasets(id))''')
    conn.commit()
    conn.close()

def register_dataset(name, source, schema_json):
    conn = sqlite3.connect(CATALOG_DB)
    conn.execute("INSERT OR REPLACE INTO datasets (name, source, schema) VALUES (?, ?, ?)",
                 (name, source, schema_json))
    conn.commit()
    conn.close()

def log_transformation(dataset_name, step_name, description):
    conn = sqlite3.connect(CATALOG_DB)
    cur = conn.execute("SELECT id FROM datasets WHERE name = ?", (dataset_name,))
    row = cur.fetchone()
    if row:
        conn.execute("INSERT INTO transformations (dataset_id, step_name, description) VALUES (?, ?, ?)",
                     (row[0], step_name, description))
        conn.commit()
    conn.close()