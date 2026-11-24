import sqlite3

DB_NAME = "contacts.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

    #Part: Database initialization
    
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

    # Part: Data insertion

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

    # Part: Tests

if __name__ == "__main__":
    init_db()
    print(inserer_contact("Ahmed Benali", "ahmed@mail.com", "0555123456", "abc123"))
    print(inserer_contact("Ahmed Benali", "ahmed@mail.com", "0555123456", "abc123"))