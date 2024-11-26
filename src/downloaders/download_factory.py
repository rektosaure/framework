# src/downloaders/download_factory.py

from .fred_downloader import FredDownloader
from .yfinance_downloader import YFinanceDownloader
from .sec_downloader import SecDownloader
from .investing_downloader import InvestingDownloader
from .ycharts_downloader import YChartsDownloader
from .cftc_downloader import CftcDownloader
from .empty_downloader import EmptyDownloader

class DownloadFactory:
    """
    Fabrique pour obtenir l'instance de downloader appropriée en fonction de la source.
    """

    @staticmethod
    def get_downloader(source):
        """
        Retourne une instance du downloader correspondant à la source spécifiée.

        Parameters
        ----------
        source : str
            La source des données (ex. 'fred', 'yfinance', etc.).

        Returns
        -------
        Downloader
            Une instance de la classe downloader appropriée.

        Raises
        ------
        ValueError
            Si la source spécifiée n'est pas prise en charge.
        """
        if source == 'fred':
            return FredDownloader()
        elif source == 'yfinance':
            return YFinanceDownloader()
        elif source == 'sec':
            return SecDownloader()
        elif source == 'investing':
            return InvestingDownloader()
        elif source == 'ycharts':
            return YChartsDownloader()
        elif source == 'cftc':
            return CftcDownloader()
        elif source == 'empty':
            return EmptyDownloader()
        else:
            raise ValueError(f"Source de téléchargement '{source}' non prise en charge.")