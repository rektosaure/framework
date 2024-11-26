import pandas as pd
import requests
import logging

class SecDownloader:
    """
    Classe pour télécharger des données depuis la SEC.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def download(self, header, ticker_url):
        """
        Télécharge les données depuis la SEC.

        Args:
            header (str): Le nom de la colonne à utiliser.
            ticker_url (str): L'URL du fichier de tickers.

        Returns:
            pd.DataFrame: Les données téléchargées.
        """
        try:
            response = requests.get(ticker_url)
            if response.status_code == 200:
                data = response.text.strip().split('\n')
                tickers = [line.split('\t') for line in data if line]
                df = pd.DataFrame(tickers, columns=['CIK', 'Ticker'])
                df.rename(columns={'CIK': header}, inplace=True)
                return df
            else:
                self.logger.error(f"Erreur lors du téléchargement des données SEC depuis {ticker_url}: Status Code {response.status_code}")
                raise ValueError(f"Erreur lors du téléchargement des données SEC depuis {ticker_url}: Status Code {response.status_code}")
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des données SEC depuis {ticker_url}: {e}")
            raise ValueError(f"Erreur lors du téléchargement des données SEC depuis {ticker_url}: {e}")