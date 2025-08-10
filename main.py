from src.dev.utils.db_utils import get_db_connection
from src.dev.services.pdf_scraper_service import BoursePDFScraper
from src.dev.config.settings import BASE_URL, PAGE_URL, DOWNLOAD_DIR

def main():
    
    db_conn = get_db_connection()
    if db_conn is None:
        print("Arrêt du script car la connexion à la base de données a échoué.")
        return
    
    
    scraper = BoursePDFScraper(
        base_url=BASE_URL,
        page_url=PAGE_URL,
        download_dir=DOWNLOAD_DIR,
        db_conn=db_conn  # <-- Ici, vous définissez db_conn en le passant en argument
    )
    