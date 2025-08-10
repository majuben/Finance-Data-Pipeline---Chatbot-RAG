import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupère les configurations depuis les variables d'environnement
BASE_URL = os.getenv("BASE_URL")
PAGE_URL = os.getenv("PAGE_URL")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
BASE_API_URL = os.getenv("BASE_API_URL")

DB_CREDS = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}