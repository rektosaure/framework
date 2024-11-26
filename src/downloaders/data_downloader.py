import abc
import logging

class DataDownloader(abc.ABC):
    """
    Classe de base abstraite pour les downloaders de données.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def download(self, header, ticker, frequency=None):
        """
        Méthode abstraite pour télécharger les données.

        Args:
            header (str): Nom de la colonne pour les données téléchargées.
            ticker (str): Symbole du ticker à télécharger.
            frequency (str, optional): Fréquence des données.

        Returns:
            pandas.DataFrame: DataFrame contenant les données téléchargées.
        """
        pass