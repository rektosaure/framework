import os
import shutil
import subprocess
import logging

class GitHubUploader:
    """
    Classe pour gérer l'upload de fichiers vers GitHub.
    """

    def __init__(self, repo_path):
        """
        Initialise le GitHubUploader avec le chemin du dépôt local.

        Args:
            repo_path (str): Chemin vers le dépôt Git local.
        """
        self.repo_path = os.path.abspath(repo_path)
        self.logger = logging.getLogger(self.__class__.__name__)

    def copy_files(self, source_folder):
        """
        Copie les fichiers du dossier source vers le dépôt Git local.

        Args:
            source_folder (str): Chemin vers le dossier contenant les fichiers à uploader.
        """
        source_folder = os.path.abspath(source_folder)
        try:
            for filename in os.listdir(source_folder):
                full_file_name = os.path.join(source_folder, filename)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, self.repo_path)
            self.logger.info("Fichiers copiés vers le dépôt local.")
        except Exception as e:
            self.logger.error(f"Erreur lors de la copie des fichiers vers le dépôt local: {e}")
            raise e

    def commit_and_push(self, commit_message="Mise à jour des données"):
        """
        Commit et push les changements vers le dépôt Git distant.

        Args:
            commit_message (str): Message du commit.
        """
        try:
            # Ajouter les fichiers au dépôt
            subprocess.check_call(['git', 'add', '.'], cwd=self.repo_path)
            # Committer les changements
            subprocess.check_call(['git', 'commit', '-m', commit_message], cwd=self.repo_path)
            # Pusher vers le dépôt distant
            subprocess.check_call(['git', 'push'], cwd=self.repo_path)

            self.logger.info("Données uploadées sur GitHub avec succès.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Une erreur s'est produite lors de l'exécution des commandes Git: {e}")
            raise e