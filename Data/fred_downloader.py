import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import logging

class FredDownloader:
    """
    Classe pour télécharger des données depuis FRED.
    """

    def __init__(self):
        """
        Initialise le FredDownloader avec une configuration de journalisation.
        """
        self.source = 'fred'
        self.logger = logging.getLogger(__name__)

    def download(self, header, ticker, frequency=None):
        """
        Télécharge les données depuis FRED pour un ticker donné.

        Args:
            header (str): Nom de la colonne pour les données téléchargées.
            ticker (str): Symbole du ticker à télécharger.
            frequency (str, optional): Fréquence des données (non utilisée dans cette implémentation).

        Returns:
            pandas.DataFrame: DataFrame contenant les données téléchargées.

        Raises:
            ValueError: Si une erreur se produit lors du téléchargement des données.
        """
        df = pd.DataFrame()
        start_date = datetime(1900, 1, 1)
        end_date = datetime.today()

        try:
            self.logger.info(f"Téléchargement des données pour le ticker '{ticker}' depuis FRED.")
            data = web.DataReader(ticker, self.source, start=start_date, end=end_date)
            df[header] = data[ticker]
            self.logger.info(f"Succès du téléchargement des données pour le ticker '{ticker}'.")
            return df

        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement des données pour le ticker '{ticker}' depuis FRED: {e}")
            raise ValueError(f"Erreur lors du téléchargement des données pour le ticker '{ticker}' depuis FRED: {e}")
