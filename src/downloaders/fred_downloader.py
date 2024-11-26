import pandas as pd
import pandas_datareader.data as web
import logging
from datetime import datetime

class FredDownloader:
    """
    Classe pour télécharger des données depuis FRED.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def download(self, header, ticker):
        """
        Télécharge les données depuis FRED.

        Args:
            header (str): Le nom de la colonne à utiliser.
            ticker (str): Le ticker FRED.

        Returns:
            pd.DataFrame: Les données téléchargées.
        """
        try:
            start = datetime(2000, 1, 1)
            end = datetime.now()
            df = web.DataReader(ticker, 'fred', start, end)
            df.reset_index(inplace=True)
            # Convertir la colonne 'DATE' en date sans l'heure
            df['DATE'] = pd.to_datetime(df['DATE']).dt.date
            # Renommer la colonne du ticker en 'header'
            df.rename(columns={ticker: header}, inplace=True)
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des données FRED pour {ticker}: {e}")
            raise ValueError(f"Erreur lors du téléchargement des données FRED pour {ticker}: {e}")