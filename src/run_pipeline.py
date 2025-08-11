from dev.services.pdf_scraper_service import BoursePDFScraper
from dev.utils.db_utils import get_db_connection
from dev.config.settings import BASE_URL, BASE_API_URL, DOWNLOAD_DIR

def main():
    db_conn = get_db_connection()
    if not db_conn:
        print("❌ Connexion DB impossible")
        return

    scraper = BoursePDFScraper(
        download_dir=DOWNLOAD_DIR,
        base_url=BASE_URL,
        db_conn=db_conn,
        base_api_url=BASE_API_URL
    )
    scraper.download_pdfs()

    # Appel d'autres services ici
    # ex: other_service.run_something()

    print("✅ Pipeline terminé")

if __name__ == "__main__":
    main()
