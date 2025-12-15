import sqlite3
from datetime import datetime

DB_NAME = "detections.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """Initialise la base et ajoute la colonne image_path si nécessaire."""
    conn = get_connection()
    cursor = conn.cursor()

    # Création de la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monnaie TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Vérifier si la colonne image_path existe déjà
    cursor.execute("PRAGMA table_info(detections)")
    columns = [col[1] for col in cursor.fetchall()]
    if "image_path" not in columns:
        cursor.execute("ALTER TABLE detections ADD COLUMN image_path TEXT")

    conn.commit()
    conn.close()

def insert_detection(monnaie, confidence, image_path=None):
    """Insère une nouvelle détection dans la base."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO detections (monnaie, confidence, image_path, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        monnaie,
        confidence,
        image_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

def get_last_detections(limit=20):
    """Récupère les dernières détections."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monnaie, confidence, image_path, timestamp
        FROM detections
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    """Retourne le nombre de détections par monnaie."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT monnaie, COUNT(*) as total
        FROM detections
        GROUP BY monnaie
        ORDER BY total DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_database():
    """Supprime toutes les entrées de la table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM detections")
    conn.commit()
    conn.close()
