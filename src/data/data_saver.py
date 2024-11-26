import abc
import os
import pandas as pd
import logging

class DataSaver(abc.ABC):
    """
    Classe de base abstraite pour sauvegarder les données traitées.
    """

    def __init__(self, output_folder):
        """
        Initialise le DataSaver avec le dossier de sortie spécifié.

        Args:
            output_folder (str): Le dossier où sauvegarder les fichiers.
        """
        self.output_folder = os.path.abspath(output_folder)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ensure_output_folder_exists()

    def _ensure_output_folder_exists(self):
        """
        Vérifie si le dossier de sortie existe, sinon le crée.
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            self.logger.info(f"Le dossier de sortie '{self.output_folder}' a été créé.")

    @abc.abstractmethod
    def save(self, data, filename):
        """
        Méthode abstraite pour sauvegarder les données.

        Args:
            data (pd.DataFrame): Le DataFrame à sauvegarder.
            filename (str): Le nom du fichier.
        """
        pass


class DataSaverCSV(DataSaver):
    """
    Classe pour sauvegarder les données traitées dans des fichiers CSV.
    """

    def save(self, data, filename):
        """
        Sauvegarde le DataFrame dans un fichier CSV dans le dossier spécifié.

        Args:
            data (pd.DataFrame): Le DataFrame à sauvegarder.
            filename (str): Le nom du fichier CSV.
        """
        try:
            file_path = os.path.join(self.output_folder, filename)
            data.to_csv(file_path)
            self.logger.info(f"Données sauvegardées dans {file_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des données en CSV: {e}")
            raise ValueError(f"Erreur lors de la sauvegarde des données en CSV: {e}")


class DataSaverJSON(DataSaver):
    """
    Classe pour sauvegarder les données traitées dans des fichiers JSON.
    """

    def save(self, data, filename):
        """
        Sauvegarde le DataFrame dans un fichier JSON dans le dossier spécifié.

        Args:
            data (pd.DataFrame): Le DataFrame à sauvegarder.
            filename (str): Le nom du fichier JSON.
        """
        try:
            file_path = os.path.join(self.output_folder, filename)
            data.to_json(file_path, orient='records', date_format='iso')
            self.logger.info(f"Données sauvegardées dans {file_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des données en JSON: {e}")
            raise ValueError(f"Erreur lors de la sauvegarde des données en JSON: {e}")


def get_data_saver(format, output_folder):
    """
    Fabrique pour obtenir une instance de DataSaver appropriée en fonction du format spécifié.

    Args:
        format (str): Le format de sauvegarde ('csv', 'json', etc.).
        output_folder (str): Le dossier où sauvegarder les fichiers.

    Returns:
        DataSaver: Une instance de DataSaver appropriée.

    Raises:
        ValueError: Si le format spécifié n'est pas supporté.
    """
    if format.lower() == 'csv':
        return DataSaverCSV(output_folder)
    elif format.lower() == 'json':
        return DataSaverJSON(output_folder)
    else:
        raise ValueError(f"Format de sauvegarde non supporté: {format}")