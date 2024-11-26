# src/downloaders/empty_downloader.py

import pandas as pd
import logging

class EmptyDownloader:
    """
    Classe pour générer des colonnes vides.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def download(self, header, ticker, freq=None, offset=None):
        """
        Génère une colonne vide avec des dates.

        Parameters
        ----------
        header : str
            Le nom de la colonne à utiliser dans le DataFrame.
        ticker : str
            (Non utilisé pour EmptyDownloader)
        freq : str, optional
            La fréquence des dates ('D', 'W', 'M', etc.).
        offset : int, optional
            Offset à appliquer sur les dates.

        Returns
        -------
        pd.DataFrame
            DataFrame contenant les colonnes 'Date' et le header spécifié avec des valeurs NaN.
        """
        try:
            freq_map = {
                'D': 'D',
                'W': 'W-MON',
                'M': 'MS',
                'Q': 'QS',
                'Y': 'AS'
            }
            if freq is None:
                freq = 'M'  # Par défaut mensuel
            date_freq = freq_map.get(freq, 'M')
            date_range = pd.date_range(end=pd.Timestamp.now(), periods=10, freq=date_freq)
            df = pd.DataFrame({
                'Date': date_range,
                header: [pd.NA] * len(date_range)
            })
            return df
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération de la colonne vide pour {header}: {e}")
            return pd.DataFrame()