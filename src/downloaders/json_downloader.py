import requests
from .data_downloader import DataDownloader

class JSONDownloader(DataDownloader):
    """
    Classe pour télécharger et charger le fichier JSON contenant les tickers.
    """

    def download(self, url, *args, **kwargs):
        """
        Télécharge le fichier JSON depuis l'URL spécifiée et le charge en tant que dictionnaire Python.

        Args:
            url (str): L'URL du fichier JSON.

        Returns:
            dict: Le contenu du fichier JSON sous forme de dictionnaire.

        Raises:
            ValueError: Si une erreur se produit lors du téléchargement ou du chargement du fichier JSON.
        """

        try:
            self.logger.info(f"Téléchargement du fichier JSON depuis {url}")
            response = requests.get(url)
            response.raise_for_status()
            tickers = response.json()
            self.logger.info("Fichier JSON téléchargé et chargé avec succès.")
            return tickers

        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"Erreur HTTP lors du téléchargement du fichier JSON: {http_err}")
            raise ValueError(f"Erreur HTTP lors du téléchargement du fichier JSON: {http_err}")

        except Exception as err:
            self.logger.error(f"Une erreur s'est produite lors du téléchargement ou du chargement du fichier JSON: {err}")
            raise ValueError(f"Une erreur s'est produite lors du téléchargement ou du chargement du fichier JSON: {err}")