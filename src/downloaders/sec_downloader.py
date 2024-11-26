# src/downloaders/sec_downloader.py

import pandas as pd
import requests
import logging

class SecDownloader:
    """
    Classe pour télécharger des données depuis la SEC.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def download(self, header, ticker_url, freq=None, offset=None):
        """
        Télécharge les données depuis la SEC.

        Parameters
        ----------
        header : str
            Le nom de la colonne à utiliser dans le DataFrame.
        ticker_url : str
            L'URL pour télécharger le fichier ticker de la SEC.
        freq : str, optional
            La fréquence des données (non applicable pour la SEC).
        offset : int, optional
            Offset à appliquer sur les dates (non applicable pour la SEC).

        Returns
        -------
        pd.DataFrame
            DataFrame contenant les données téléchargées avec les colonnes 'Date' et le header spécifié.
        """
        try:
            response = requests.get(ticker_url)
            if response.status_code == 200:
                tickers = response.text.splitlines()
                # Exemple simplifié: Créer un DataFrame avec les tickers
                df = pd.DataFrame(tickers, columns=[header])
                df['Date'] = pd.Timestamp.now().normalize()
                return df
            else:
                self.logger.error(f"Erreur lors du téléchargement des tickers SEC: Status Code {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des données SEC: {e}")
            return pd.DataFrame()