import sqlite3

DB_NAME = "contacts.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

    # Part: Database Initialization

def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL,
                telephone TEXT,
                hash TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rejets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                email TEXT,
                telephone TEXT,
                raison TEXT
            )
            """
        )

    # Part: DataBase Insertion

def inserer_contact(nom, email, telephone, hash_value):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO contacts (nom, email, telephone, hash) VALUES (?, ?, ?, ?)",
                (nom, email, telephone, hash_value),
            )
        return True
    except sqlite3.IntegrityError:
        return False

    # Part: Check if hash exists

def hash_existe(hash_value):
    with get_connection() as conn:
        ligne = conn.execute(
            "SELECT 1 FROM contacts WHERE hash = ?", (hash_value,)
        ).fetchone()
    return ligne is not None

    # Part: List contacts

def lister_contacts():
    with get_connection() as conn:
        return conn.execute("SELECT nom, email, telephone FROM contacts").fetchall()

    # Part: Save Rejected contacts

def enregistrer_rejet(nom, email, telephone, raison):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO rejets (nom, email, telephone, raison) VALUES (?, ?, ?, ?)",
            (nom, email, telephone, raison),
        )