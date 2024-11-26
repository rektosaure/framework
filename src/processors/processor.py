# src/processors/processor.py

import pandas as pd
import logging

class DataProcessor:
    """
    Classe pour traiter les données téléchargées.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def adjust_date(self, category, source, freq, offset, df):
        """
        Ajuste les dates des données en fonction de la fréquence et de l'offset.

        Args:
            category (str): Nom de la catégorie.
            source (str): Source des données.
            freq (str): Fréquence des données.
            offset (int): Offset à appliquer.
            df (pd.DataFrame): DataFrame à ajuster.

        Returns:
            pd.DataFrame: DataFrame ajustée.
        """
        try:
            if 'Date' not in df.columns:
                raise ValueError("La colonne 'Date' est manquante dans le DataFrame.")

            df['Date'] = pd.to_datetime(df['Date']).normalize()

            # Ajustements spécifiques basés sur la source et le nom
            if source == 'investing' and category in ['USA_PMI', 'USA_NMI', 'WORLD_PMI', 'WORLD_NMI']:
                df.loc[df['Date'].dt.day > 15, 'Date'] += pd.to_timedelta(15, unit='D')

            if source == 'investing' and category == 'EUROPE_ESI':
                df.loc[df['Date'].dt.day < 15, 'Date'] -= pd.to_timedelta(15, unit='D')

            if source == 'investing' and category == 'USA_UMCSI':
                df.loc[df['Date'].dt.day < 15, 'Date'] -= pd.to_timedelta(15, unit='D')

            # Ajuster selon la fréquence
            if freq == 'W':  # Premier jour de la semaine (lundi)
                df['Date'] = df['Date'].dt.to_period('W').start_time
            elif freq == 'M':  # Premier jour du mois
                df['Date'] = df['Date'].dt.to_period('M').start_time
            elif freq == 'Q':  # Premier jour du trimestre
                df['Date'] = df['Date'].dt.to_period('Q').start_time
            elif freq == 'Y':  # Premier jour de l'année
                df['Date'] = df['Date'].dt.to_period('Y').start_time

            # Appliquer l'offset s'il est spécifié
            if offset is not None:
                df['Date'] += pd.DateOffset(months=offset)

            # Supprimer les doublons en gardant la dernière occurrence
            df = df.drop_duplicates(subset='Date', keep='last')

            return df

        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajustement des dates pour {category}: {e}")
            raise ValueError(f"Erreur lors de l'ajustement des dates pour {category}: {e}")