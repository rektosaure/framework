import logging
import shutil
import os
import pandas as pd  # Importation de pandas
from data import DataProcessor, get_data_saver
from downloaders import get_downloader
from uploaders.github_uploader import GitHubUploader  # Importation de la classe

def configure_logging():
    """
    Configure le logger pour l'application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main(tickers_url, gitrepo_owner, gitrepo_name, gitrepo_authkey, gitrepo_folder=""):
    """
    Fonction principale pour télécharger, traiter, sauvegarder les données et les uploader sur GitHub.

    Args:
        tickers_url (str): URL du fichier JSON des tickers.
        gitrepo_owner (str): Nom d'utilisateur ou organisation propriétaire du dépôt GitHub.
        gitrepo_name (str): Nom du dépôt GitHub.
        gitrepo_authkey (str): Token d'authentification GitHub (Personal Access Token).
        gitrepo_folder (str): Dossier cible dans le dépôt GitHub où les fichiers seront uploadés.
                              Par défaut, les fichiers sont uploadés à la racine du dépôt.
    """
    # Configuration du logger
    configure_logging()
    logger = logging.getLogger(__name__)

    # Définition du répertoire de sortie temporaire
    output_folder = 'output'  # Répertoire temporaire pour les données

    # Création des instances des classes
    data_processor = DataProcessor()
    format_sauvegarde = 'csv'  # Défini en 'csv'
    data_saver_class = get_data_saver(format_sauvegarde)
    data_saver = data_saver_class(output_folder=output_folder)

    # Téléchargement du fichier JSON en utilisant la fabrique
    try:
        json_downloader = get_downloader('json')
        tickers = json_downloader.download(tickers_url)
    except ValueError as e:
        logger.error(f"Erreur lors du téléchargement du fichier JSON: {e}")
        return

    # Parcours des catégories et des entrées
    for category_name, entries in tickers.items():
        logger.info(f"Traitement de la catégorie : {category_name}")
        category_df = None  # Initialiser à None pour la fusion
        for entry in entries:
            source = entry['Source']
            header = entry['Header']
            ticker = entry['Ticker']
            frequency = entry['Frequency']
            offset = entry['Offset']

            logger.info(f"Téléchargement des données pour {header} ({ticker}) depuis {source}")

            try:
                # Obtenir le downloader approprié
                downloader = get_downloader(source)

                # Téléchargement des données
                data = downloader.download(header, ticker)

                # Ajustement des dates si nécessaire
                data = data_processor.adjust_date(data, frequency, offset)

                # Vérifier que la colonne DATE existe
                if 'DATE' not in data.columns:
                    logger.error(f"La colonne 'DATE' est manquante dans les données pour {header}.")
                    continue

                # Assurez-vous que la colonne DATE est au format datetime.date
                data['DATE'] = pd.to_datetime(data['DATE']).dt.date

                # Si category_df est None, initialiser avec les données actuelles
                if category_df is None:
                    category_df = data
                else:
                    # Fusionner les données sur la colonne DATE
                    category_df = pd.merge(category_df, data, on='DATE', how='outer')

            except ValueError as e:
                logger.error(f"Erreur lors du traitement des données pour {header}: {e}")
            except Exception as e:
                logger.error(f"Une erreur inattendue s'est produite pour {header}: {e}")

        # Sauvegarde des données de la catégorie si non vide
        if category_df is not None and not category_df.empty:
            # Trier les données par DATE
            category_df.sort_values(by='DATE', inplace=True)
            # Réinitialiser l'index
            category_df.reset_index(drop=True, inplace=True)
            filename = f"{category_name}.csv"
            data_saver.save(category_df, filename)
        else:
            logger.warning(f"Aucune donnée à sauvegarder pour la catégorie {category_name}")

    # Après le traitement, uploader les données sur GitHub
    try:
        # Initialiser le GitHubUploader avec les informations du dépôt et la clé d'authentification
        github_uploader = GitHubUploader(
            gitrepo_owner=gitrepo_owner,
            gitrepo_name=gitrepo_name,
            gitrepo_authkey=gitrepo_authkey
        )

        # Upload des fichiers vers le dépôt GitHub
        github_uploader.upload_files(source_folder=output_folder, gitrepo_folder=gitrepo_folder)

    except Exception as e:
        logger.error(f"Erreur lors de l'upload sur GitHub: {e}")

    # Supprimer le répertoire temporaire
    try:
        shutil.rmtree(output_folder)
        logger.info(f"Le répertoire temporaire '{output_folder}' a été supprimé.")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du répertoire temporaire '{output_folder}': {e}")