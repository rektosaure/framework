# src/downloaders/yfinance_downloader.py

import yfinance as yf
import pandas as pd
import logging

class YFinanceDownloader:
    """
    Classe pour télécharger des données depuis Yahoo Finance.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def download(self, header, ticker, freq='D', offset=None):
        """
        Télécharge les données depuis Yahoo Finance.

        Parameters
        ----------
        header : str
            Le nom de la colonne à utiliser dans le DataFrame.
        ticker : str
            Le ticker Yahoo Finance à télécharger.
        freq : str, optional
            La fréquence des données ('D', 'W', 'M', 'Q', 'Y').
        offset : int, optional
            Offset à appliquer sur les dates (par défaut est None).

        Returns
        -------
        pd.DataFrame
            DataFrame contenant les données téléchargées avec les colonnes 'Date' et le header spécifié.
        """
        try:
            df = yf.download(ticker, progress=False)
            df.reset_index(inplace=True)
            df = df[['Date', 'Close']].rename(columns={'Close': header})
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des données Yahoo Finance pour {ticker}: {e}")
            return pd.DataFrame()