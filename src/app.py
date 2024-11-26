import logging
import shutil
import os
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

def main(tickers_url, git_repo_path, github_auth_key):
    """
    Fonction principale pour télécharger, traiter, sauvegarder les données et les uploader sur GitHub.

    Args:
        tickers_url (str): URL du fichier JSON des tickers.
        git_repo_path (str): Chemin vers le dépôt Git local.
        github_auth_key (str): Clé d'authentification GitHub (par exemple, un token d'accès personnel).
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

                # Sauvegarde des données
                filename = f"{category_name}_{header}.csv"
                data_saver.save(data, filename)

            except ValueError as e:
                logger.error(f"Erreur lors du traitement des données pour {header}: {e}")
            except Exception as e:
                logger.error(f"Une erreur inattendue s'est produite pour {header}: {e}")

    # Après le traitement, uploader les données sur GitHub
    try:
        # Initialiser le GitHubUploader avec le chemin vers votre dépôt local et la clé d'authentification
        github_uploader = GitHubUploader(repo_path=git_repo_path, auth_key=github_auth_key)

        # Copier les fichiers vers le dépôt
        github_uploader.copy_files(output_folder)

        # Commit et push des changements
        github_uploader.commit_and_push(commit_message="Mise à jour des données")

    except Exception as e:
        logger.error(f"Erreur lors de l'upload sur GitHub: {e}")

    # Supprimer le répertoire temporaire
    try:
        shutil.rmtree(output_folder)
        logger.info(f"Le répertoire temporaire '{output_folder}' a été supprimé.")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du répertoire temporaire '{output_folder}': {e}")