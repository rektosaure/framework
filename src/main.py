import argparse
from app import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Télécharge, traite et upload des données sur GitHub.")
    parser.add_argument('--tickers_url', type=str, required=True, help='URL du fichier JSON des tickers.')
    parser.add_argument('--gitrepo_owner', type=str, required=True, help='Nom d\'utilisateur ou organisation propriétaire du dépôt GitHub.')
    parser.add_argument('--gitrepo_name', type=str, required=True, help='Nom du dépôt GitHub.')
    parser.add_argument('--gitrepo_authkey', type=str, required=True, help='Clé d\'authentification GitHub (Personal Access Token).')
    parser.add_argument('--gitrepo_folder', type=str, default="", help='Dossier cible dans le dépôt GitHub où les fichiers seront uploadés.')

    args = parser.parse_args()

    main(
        tickers_url=args.tickers_url,
        gitrepo_owner=args.gitrepo_owner,
        gitrepo_name=args.gitrepo_name,
        gitrepo_authkey=args.gitrepo_authkey,
        gitrepo_folder=args.gitrepo_folder
    )