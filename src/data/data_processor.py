import pandas as pd
import logging

class DataProcessor:
    """
    Classe pour traiter les données téléchargées, y compris l'ajustement des dates.
    """

    def __init__(self):
        """
        Initialise le DataProcessor avec une configuration de journalisation.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

    def adjust_date(self, data, frequency, offset):
        """
        Ajuste les dates du DataFrame en fonction de la fréquence et de l'offset spécifiés.

        Args:
            data (pd.DataFrame): Le DataFrame contenant les données.
            frequency (str): La fréquence des données ('D', 'W', 'M', 'Q', 'Y').
            offset (int or None): Un décalage en mois à appliquer aux dates.

        Returns:
            pd.DataFrame: Le DataFrame avec les dates ajustées.
        """

        try:
            data = data.copy()
            data.index = pd.to_datetime(data.index)  # Assure que l'index est de type DateTime
            data.index.name = 'Date'

            # Ajuste la date en fonction de la fréquence
            if frequency == 'W':
                data.index = data.index.to_period('W').start_time
            elif frequency == 'M':
                data.index = data.index.to_period('M').start_time
            elif frequency == 'Q':
                data.index = data.index.to_period('Q').start_time
            elif frequency == 'Y':
                data.index = data.index.to_period('Y').start_time

            # Applique l'offset si spécifié
            if offset is not None:
                data.index += pd.DateOffset(months=offset)

            self.logger.info("Dates ajustées avec succès.")
            return data

        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajustement des dates: {e}")
            raise ValueError(f"Erreur lors de l'ajustement des dates: {e}")