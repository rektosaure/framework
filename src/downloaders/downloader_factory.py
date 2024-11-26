from .fred_downloader import FredDownloader
from .json_downloader import JSONDownloader

def get_downloader(source):
    """
    Fabrique pour obtenir une instance de DataDownloader appropriée en fonction de la source spécifiée.

    Args:
        source (str): La source des données ('fred', 'json', etc.).

    Returns:
        DataDownloader: Une instance de DataDownloader appropriée.

    Raises:
        ValueError: Si la source spécifiée n'est pas supportée.
    """
    if source == 'fred':
        return FredDownloader()
    elif source == 'json':
        return JSONDownloader()
    else:
        raise ValueError(f"Source non supportée : {source}")