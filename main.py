from src.dev.utils.db_utils import get_db_connection
from src.dev.services.pdf_scraper_service import BoursePDFScraper
from src.dev.config.settings import BASE_URL, BASE_API_URL, DOWNLOAD_DIR

def main():
    db_conn = get_db_connection()
    if db_conn is None:
        print("❌ Arrêt du script car la connexion à la base de données a échoué.")
        return

    scraper = BoursePDFScraper(
        download_dir=DOWNLOAD_DIR,
        base_url=BASE_URL,
        db_conn=db_conn,
        base_api_url=BASE_API_URL
    )

    scraper.download_pdfs()
    print("✅ Téléchargement terminé.")

if __name__ == "__main__":
    main()
 
    
    