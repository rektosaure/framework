# src/uploaders/github_uploader.py

import os
from github import Github
import logging

class GitHubUploader:
    """
    Classe pour uploader des fichiers sur GitHub.
    """

    def __init__(self, repo_owner, repo_name, repo_token):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_token = repo_token
        self.github = Github(self.repo_token)
        try:
            self.repo = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")
            self.logger.info(f"Connecté au dépôt GitHub {self.repo_owner}/{self.repo_name}.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la connexion au dépôt GitHub {self.repo_owner}/{self.repo_name}: {e}")
            raise ValueError(f"Erreur lors de la connexion au dépôt GitHub {self.repo_owner}/{self.repo_name}: {e}")

    def upload_files(self, source_folder, target_folder=""):
        """
        Upload les fichiers d'un répertoire local vers un répertoire spécifique dans GitHub.

        Args:
            source_folder (str): Chemin du répertoire local contenant les fichiers à uploader.
            target_folder (str): Chemin du répertoire cible dans le dépôt GitHub.
        """
        try:
            for file_name in os.listdir(source_folder):
                if not file_name.startswith('.'):
                    file_path = os.path.join(source_folder, file_name)
                    with open(file_path, 'r') as file:
                        content = file.read()

                    if target_folder:
                        github_path = os.path.join(target_folder, file_name).replace("\\", "/")
                    else:
                        github_path = file_name

                    try:
                        existing_file = self.repo.get_contents(github_path)
                        self.repo.update_file(existing_file.path, f"Updating {file_name}", content, existing_file.sha)
                        self.logger.info(f"Le fichier '{file_name}' a été mis à jour sur GitHub.")
                    except:
                        self.repo.create_file(github_path, f"Création de {file_name}", content)
                        self.logger.info(f"Le fichier '{file_name}' a été créé sur GitHub.")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'upload des fichiers sur GitHub : {e}")
            raise ValueError(f"Erreur lors de l'upload des fichiers sur GitHub : {e}")