# src/main.py

import argparse
from app import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Télécharge, traite et upload des données sur GitHub.")
    parser.add_argument('--tickers_url', type=str, required=True, help='URL du fichier JSON des tickers.')
    parser.add_argument('--git_repo_path', type=str, required=True, help='Chemin vers le dépôt Git local.')
    parser.add_argument('--github_auth_key', type=str, required=True, help='Clé d\'authentification GitHub (PAT).')

    args = parser.parse_args()

    main(tickers_url=args.tickers_url, git_repo_path=args.git_repo_path, github_auth_key=args.github_auth_key)