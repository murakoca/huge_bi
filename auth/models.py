import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'viewer')''')
    c.execute('''CREATE TABLE IF NOT EXISTS workspaces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    owner_id INTEGER,
                    FOREIGN KEY(owner_id) REFERENCES users(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS workspace_members (
                    workspace_id INTEGER,
                    user_id INTEGER,
                    permission TEXT DEFAULT 'read',
                    PRIMARY KEY(workspace_id, user_id))''')
    conn.commit()
    conn.close()

def create_user(username, password, role='viewer'):
    conn = sqlite3.connect(DATABASE)
    hash = generate_password_hash(password)
    try:
        conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                     (username, hash, role))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DATABASE)
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        return {'id': user[0], 'username': user[1], 'role': user[3]}
    return None