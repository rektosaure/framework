import logging
import shutil
import os
from data import DataProcessor, get_data_saver
from downloaders import get_downloader
from uploaders.github_uploader import GitHubUploader

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

    # Dictionnaire pour stocker les DataFrames par catégorie
    category_data = {}

    # Parcours des catégories et des entrées
    for category_name, entries in tickers.items():
        logger.info(f"Traitement de la catégorie : {category_name}")
        category_df = pd.DataFrame()  # DataFrame vide pour la catégorie
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

                # Ajout des données au DataFrame de la catégorie
                category_df = pd.concat([category_df, data], ignore_index=True)

            except ValueError as e:
                logger.error(f"Erreur lors du traitement des données pour {header}: {e}")
            except Exception as e:
                logger.error(f"Une erreur inattendue s'est produite pour {header}: {e}")

        # Sauvegarde des données de la catégorie si non vide
        if not category_df.empty:
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