import psycopg2
from src.dev.config.settings import DB_CREDS

def get_db_connection():
    """Établit et retourne une connexion à la base de données."""
    try:
        conn = psycopg2.connect(**DB_CREDS)
        return conn
    except psycopg2.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None