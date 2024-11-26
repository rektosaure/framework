import os
import logging
from github import Github, GithubException

class GitHubUploader:
    """
    Classe pour gérer l'upload de fichiers vers un dépôt GitHub existant via l'API GitHub.
    """

    def __init__(self, gitrepo_owner, gitrepo_name, gitrepo_authkey):
        """
        Initialise le GitHubUploader avec les informations du dépôt et la clé d'authentification.

        Args:
            gitrepo_owner (str): Nom d'utilisateur ou organisation propriétaire du dépôt.
            gitrepo_name (str): Nom du dépôt GitHub.
            gitrepo_authkey (str): Token d'authentification GitHub (Personal Access Token).
        """
        self.gitrepo_owner = gitrepo_owner
        self.gitrepo_name = gitrepo_name
        self.gitrepo_authkey = gitrepo_authkey
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            self.github = Github(self.gitrepo_authkey)
            self.repo = self.github.get_repo(f"{self.gitrepo_owner}/{self.gitrepo_name}")
            self.logger.info(f"Connecté au dépôt GitHub: {self.gitrepo_owner}/{self.gitrepo_name}")
        except GithubException as e:
            self.logger.error(f"Erreur lors de la connexion au dépôt GitHub: {e}")
            raise e

    def upload_files(self, source_folder, gitrepo_folder=""):
        """
        Upload les fichiers du dossier source vers le dépôt GitHub dans le dossier cible.

        Args:
            source_folder (str): Chemin vers le dossier contenant les fichiers à uploader.
            gitrepo_folder (str): Chemin relatif dans le dépôt GitHub où les fichiers seront uploadés.
                                   Par défaut, les fichiers sont uploadés à la racine du dépôt.
        """
        source_folder = os.path.abspath(source_folder)
        try:
            for filename in os.listdir(source_folder):
                full_file_path = os.path.join(source_folder, filename)
                if os.path.isfile(full_file_path):
                    with open(full_file_path, "rb") as file:
                        content = file.read()
                    # Définir le chemin cible dans le dépôt
                    if gitrepo_folder:
                        target_path = f"{gitrepo_folder}/{filename}"
                    else:
                        target_path = filename
                    try:
                        # Vérifier si le fichier existe déjà
                        existing_file = self.repo.get_contents(target_path)
                        # Mettre à jour le fichier existant
                        self.repo.update_file(
                            path=existing_file.path,
                            message=f"Mise à jour de {filename}",
                            content=content,
                            sha=existing_file.sha
                        )
                        self.logger.info(f"Mise à jour du fichier: {target_path}")
                    except GithubException as e:
                        if e.status == 404:
                            # Créer un nouveau fichier
                            self.repo.create_file(
                                path=target_path,
                                message=f"Ajout de {filename}",
                                content=content
                            )
                            self.logger.info(f"Ajout du fichier: {target_path}")
                        else:
                            self.logger.error(f"Erreur lors de l'upload du fichier {filename}: {e}")
                            raise e
            self.logger.info("Tous les fichiers ont été uploadés avec succès.")
        except Exception as e:
            self.logger.error(f"Erreur lors de l'upload des fichiers: {e}")
            raise e