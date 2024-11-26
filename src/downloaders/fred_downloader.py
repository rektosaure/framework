# src/downloaders/fred_downloader.py

import pandas as pd
import pandas_datareader.data as web
import logging

class FredDownloader:
    """
    Classe pour télécharger des données depuis FRED.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def download(self, header, ticker, freq=None, offset=None):
        """
        Télécharge les données depuis FRED.

        Parameters
        ----------
        header : str
            Le nom de la colonne à utiliser dans le DataFrame.
        ticker : str
            Le ticker FRED à télécharger.
        freq : str, optional
            La fréquence des données (par défaut est 'D' pour quotidien).
        offset : int, optional
            Offset à appliquer sur les dates (par défaut est None).

        Returns
        -------
        pd.DataFrame
            DataFrame contenant les données téléchargées avec les colonnes 'Date' et le header spécifié.
        """
        try:
            df = web.DataReader(ticker, 'fred')
            df.reset_index(inplace=True)
            df.rename(columns={ticker: header}, inplace=True)
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des données FRED pour {ticker}: {e}")
            return pd.DataFrame()