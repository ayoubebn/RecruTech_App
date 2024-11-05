import sqlite3
from config import Config

def create_database_tables():
    # Connexion à SQLite
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)  # Define `SQLITE_DB_PATH` in your config for SQLite database file path
    cursor = conn.cursor()
    
    # Création de la table users si elle n'existe pas déjà
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Création de la table job_postings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_postings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        requirements TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Création de la table applications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_id INTEGER,
        cv_text TEXT,
        score REAL,
        evaluation_details BLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (job_id) REFERENCES job_postings(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    
    print("Tables créées avec succès en SQLite!")

if __name__ == "__main__":
    create_database_tables()
