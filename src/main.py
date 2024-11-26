# main.py

import logging
from downloader_factory import get_downloader
from data import DataProcessor, get_data_saver  # Import mis à jour

def configure_logging():
    """
    Configure le logger pour l'application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    # Configuration du logger
    configure_logging()
    logger = logging.getLogger(__name__)

    # URL du fichier JSON
    json_url = 'https://raw.githubusercontent.com/rektosaure/framework/refs/heads/main/tickers.json'

    # Création des instances des classes
    data_processor = DataProcessor()

    # Choix du format de sauvegarde
    format_sauvegarde = 'csv'  # Peut être 'csv' ou 'json'
    data_saver = get_data_saver(format_sauvegarde, output_folder='data')

    # Téléchargement du fichier JSON en utilisant la fabrique
    try:
        json_downloader = get_downloader('json')
        tickers = json_downloader.download(json_url)
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
                if format_sauvegarde == 'csv':
                    filename = f"{category_name}_{header}.csv"
                elif format_sauvegarde == 'json':
                    filename = f"{category_name}_{header}.json"
                else:
                    filename = f"{category_name}_{header}"

                data_saver.save(data, filename)

            except ValueError as e:
                logger.error(f"Erreur lors du traitement des données pour {header}: {e}")
            except Exception as e:
                logger.error(f"Une erreur inattendue s'est produite pour {header}: {e}")

if __name__ == "__main__":
    main()