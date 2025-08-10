import os
import requests
from datetime import datetime
import certifi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BoursePDFScraper:
    def __init__(self, download_dir, base_url, db_conn, base_api_url=None, limit=9):
        self.base_api_url = base_api_url 
        self.base_url = base_url
        self.download_dir = download_dir
        self.db_conn = db_conn
        self.limit = limit

        if not self.base_api_url:
            raise ValueError("BASE_API_URL manquant dans l'environnement ou en paramètre.")

    def _is_already_downloaded(self, url):
        """Vérifie si le PDF est déjà enregistré en base"""
        cur = self.db_conn.cursor()
        cur.execute("SELECT 1 FROM editions_statistiques WHERE url = %s", (url,))
        return cur.fetchone() is not None

    def _mark_as_downloaded(self, filename, url):
        """Ajoute l'entrée en base"""
        cur = self.db_conn.cursor()
        cur.execute(
            "INSERT INTO editions_statistiques (filename, url, download_date) VALUES (%s, %s, %s)",
            (filename, url, datetime.now())
        )
        self.db_conn.commit()
        
 

    def safe_get(self, url):
        try:
            return requests.get(url, verify=certifi.where(), timeout=10)
        except requests.exceptions.SSLError:
            print("[WARNING] SSL verification failed. Retrying without certificate verification...")
            return requests.get(url, verify=False, timeout=10)


    def get_pdf_links_with_stop(self):
        """Récupère tous les liens PDF jusqu'à trouver un déjà téléchargé"""
        offset = 0
        all_links = []
        stop_flag = False

        while not stop_flag:
            api_url = f"{self.base_api_url}&page[offset]={offset}&page[limit]={self.limit}"
            resp = self.safe_get(api_url)
            resp.raise_for_status()
            data = resp.json()

            pdf_links = []
            for item in data.get("included", []):
                if item["type"] == "file--document":
                    file_url = item["attributes"]["uri"]["url"]
                    if file_url.lower().endswith(".pdf"):
                        full_url = self.base_url + file_url

                        # Stop complet si on tombe sur un fichier déjà téléchargé
                        if self._is_already_downloaded(full_url):
                            stop_flag = True
                            break

                        pdf_links.append(full_url)

            if not pdf_links:
                break  # plus de fichiers trouvés

            all_links.extend(pdf_links)
            offset += self.limit

        return all_links

    def download_pdfs(self):
        links = self.get_pdf_links_with_stop()
        for url in links:
            filename = url.split("/")[-1]
            file_path = os.path.join(self.download_dir, filename)

            print(f"⬇ Téléchargement : {filename}")
            try:
                r = self.safe_get(url)
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"⚠️ Impossible de télécharger {filename} : {e}")
                continue  # passe au fichier suivant
            except Exception as e:
                print(f"⚠️ Erreur lors du téléchargement de {filename} : {e}")
                continue
        
            with open(file_path, "wb") as f:
                f.write(r.content)

            self._mark_as_downloaded(filename, url)
            print(f"✅ Sauvegardé : {filename}")


