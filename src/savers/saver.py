# src/savers/saver.py

import os
import pandas as pd
import logging

class DataSaver:
    """
    Classe pour sauvegarder les données dans des fichiers CSV.
    """

    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.logger = logging.getLogger(self.__class__.__name__)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def save_csv(self, category, df):
        """
        Sauvegarde le DataFrame dans un fichier CSV.

        Args:
            category (str): Nom du fichier CSV.
            df (pd.DataFrame): DataFrame à sauvegarder.
        """
        try:
            if category == "SEC_CIK":
                df = df.sort_values(by='Date', ascending=True)
            else:
                df = df.sort_values(by='Date', ascending=False)

            df = df.reset_index(drop=True)
            filename = os.path.join(self.output_folder, f"{category}.csv")
            df.to_csv(filename, index=False)
            self.logger.info(f"Données pour {category} sauvegardées dans {filename}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des données pour {category}: {e}")
            raise ValueError(f"Erreur lors de la sauvegarde des données pour {category}: {e}")