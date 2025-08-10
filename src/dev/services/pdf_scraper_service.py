import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

class BoursePDFScraper:
    def __init__(self, BASE_URL, PAGE_URL, DOWNLOAD_DIR, db_conn=None):
        self.base_url = BASE_URL
        self.page_url = PAGE_URL
        self.download_dir = DOWNLOAD_DIR
        self.db_conn = db_conn

    def _is_already_downloaded(self, url):
        cur = self.db_conn.cursor()
        cur.execute("SELECT 1 FROM editions_statistiques WHERE url = %s", (url,))
        return cur.fetchone() is not None

    def _mark_as_downloaded(self, filename, url):
        cur = self.db_conn.cursor()
        cur.execute(
            "INSERT INTO editions_statistiques (filename, url, download_date) VALUES (%s, %s, %s)",
            (filename, url, datetime.now())
        )
        self.db_conn.commit()

    def get_pdf_links(self):
        offset = 0
        limit = 9
        resp = requests.get(self.page_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            if a["href"].lower().endswith(".pdf"):
                full_url = a["href"]
                if not full_url.startswith("http"):
                    full_url = self.base_url + full_url
                links.append(full_url)
        return links

    def download_pdfs(self):
        links = self.get_pdf_links()
        for url in links:
            filename = url.split("/")[-1]
            file_path = os.path.join(self.download_dir, filename)

            if self._is_already_downloaded(url):
                print(f"⏭ Déjà téléchargé : {filename}")
                continue

            print(f"⬇ Téléchargement : {filename}")
            r = requests.get(url)
            with open(file_path, "wb") as f:
                f.write(r.content)

            self._mark_as_downloaded(filename, url)
