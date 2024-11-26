import abc
import logging

class DataDownloader(abc.ABC):
    """
    Classe de base abstraite pour les downloaders de données.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def download(self, *args, **kwargs):
        """
        Méthode abstraite pour télécharger les données.

        Doit être implémentée par les classes dérivées.
        """
        pass