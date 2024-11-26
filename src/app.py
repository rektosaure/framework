# src/app.py

import json
import os
import time
import random
import shutil
import logging
import requests

from downloaders.download_factory import DownloadFactory
from processors.processor import DataProcessor
from savers.saver import DataSaver
from uploaders.github_uploader import GitHubUploader

def load_tickers(tickers_url):
    response = requests.get(tickers_url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Erreur lors du téléchargement de tickers.json: Status Code {response.status_code}")
        raise ValueError(f"Erreur lors du téléchargement de tickers.json: Status Code {response.status_code}")

def main(tickers_url, gitrepo_owner, gitrepo_name, gitrepo_authkey, gitrepo_folder):
    # Configurer le logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("App")
    
    try:
        # Charger les tickers depuis l'URL
        tickers = load_tickers(tickers_url)
        logger.info("Tickers chargés avec succès.")
        
        # Configurer les paramètres GitHub
        github_uploader = GitHubUploader(
            repo_owner=gitrepo_owner,
            repo_name=gitrepo_name,
            repo_token=gitrepo_authkey
        )
        
        # Initialiser les autres composants
        data_processor = DataProcessor()
        data_saver = DataSaver("data")
        
        while True:
            logger.info("Début du processus de téléchargement et de traitement des données.")
            
            # Créer le répertoire de sortie
            if os.path.exists("data"):
                try:
                    shutil.rmtree("data")
                    logger.info("Répertoire 'data' supprimé.")
                except Exception as e:
                    logger.error(f"Erreur lors de la suppression du répertoire 'data': {e}")
            
            os.makedirs("data", exist_ok=True)
            logger.info("Répertoire 'data' créé.")
            
            # Parcourir chaque catégorie de tickers
            for category, ticker_info_list in tickers.items():
                logger.info(f"Traitement de la catégorie: {category}")
                dfs = []
                
                for ticker_info in ticker_info_list:
                    header = ticker_info.get('Header')
                    source = ticker_info.get('Source')
                    freq = ticker_info.get('Frequency')
                    offset = ticker_info.get('Offset')
                    
                    downloader = DownloadFactory.get_downloader(source)
                    
                    if source == 'sec':
                        ticker_url = ticker_info.get('Ticker')
                        df = downloader.download(header, ticker_url, freq, offset)
                    else:
                        ticker = ticker_info.get('Ticker')
                        df = downloader.download(header, ticker, freq, offset)
                    
                    if df is not None and not df.empty:
                        df = data_processor.adjust_date(category, source, freq, offset, df)
                        dfs.append(df)
                        logger.info(f"Données téléchargées et traitées pour {header} dans la catégorie {category}.")
                    else:
                        logger.warning(f"Aucune donnée téléchargée pour {header} dans la catégorie {category}.")
                
                if dfs:
                    # Fusionner les DataFrames sur la colonne 'Date'
                    merged_df = dfs[0]
                    for df in dfs[1:]:
                        merged_df = merged_df.merge(df, on='Date', how='outer')
                    
                    # Sauvegarder le DataFrame fusionné en CSV
                    data_saver.save_csv(category, merged_df)
                    logger.info(f"Données sauvegardées pour la catégorie '{category}'.")
                else:
                    logger.warning(f"Aucune donnée à sauvegarder pour la catégorie '{category}'.")
            
            # Uploader les fichiers CSV sur GitHub
            try:
                github_uploader.upload_files("data", gitrepo_folder)
                logger.info("Fichiers CSV uploadés avec succès sur GitHub.")
            except Exception as e:
                logger.error(f"Erreur lors de l'upload sur GitHub: {e}")
            
            # Pause avant la prochaine exécution
            sleep_duration = 6 * 3600  # 6 heures en secondes
            variation = random.randint(-900, 900)  # ±15 minutes en secondes
            total_sleep = sleep_duration + variation
            logger.info(f"Pause de {total_sleep/3600:.2f} heures avant la prochaine exécution.")
            time.sleep(total_sleep)
    
    except Exception as e:
        logger.error(f"Erreur critique dans l'application: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 6:
        print("Usage: python src/app.py <tickers_url> <gitrepo_owner> <gitrepo_name> <gitrepo_authkey> <gitrepo_folder>")
        sys.exit(1)
    
    tickers_url = sys.argv[1]
    gitrepo_owner = sys.argv[2]
    gitrepo_name = sys.argv[3]
    gitrepo_authkey = sys.argv[4]
    gitrepo_folder = sys.argv[5]
    
    main(tickers_url, gitrepo_owner, gitrepo_name, gitrepo_authkey, gitrepo_folder)