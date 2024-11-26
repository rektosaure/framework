import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from .data_downloader import DataDownloader

class FredDownloader(DataDownloader):
    """
    Classe pour télécharger des données depuis FRED.
    """

    def __init__(self):
        super().__init__()
        self.source = 'fred'

    def download(self, header, ticker, frequency=None):
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