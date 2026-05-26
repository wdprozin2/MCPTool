import requests
import json
import time
import sys
import os
import shutil
import zipfile
import subprocess

from src.decoration.print_banner import print_banner
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities
from src.decoration.paint import paint


class MCPToolUpdater:
    @staticmethod
    def show_banner_update():
        """
        This method displays an update banner and checks for updates.

        It first determines the appropriate update banner to show based on the environment.
        Then, it displays the banner, checks for updates, and takes appropriate action based on the result.
        """
        
        try:
            # Get the update banner.
            update_banner_name = 'update' if not CheckUtilities.check_termux() else 'update_termux'

            # Show the banner.
            print_banner(
                update_banner_name,
                GetUtilities.get_translated_text(['banners', 'update', 'title']),
                GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                '', '', '', '', ''
            )

            time.sleep(1)

            # Check for updates.
            if MCPToolUpdater.check_update():
                # Show the banner with information about a new version.
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'newVersion']),
                    '', '', '', ''
                )

                time.sleep(1)

                # Attempt automatic update
                if MCPToolUpdater.perform_update():
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aReiniciando o MCPTool para aplicar as atualizações...')
                    time.sleep(3)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    repo = JsonManager.get('githubRepository') or 'wrrulos/MCPTool'
                    # Show the banner with a link to the new version.
                    print_banner(
                        update_banner_name,
                        GetUtilities.get_translated_text(['banners', 'update', 'title']),
                        GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                        GetUtilities.get_translated_text(['banners', 'update', 'newVersion']),
                        GetUtilities.get_translated_text(['banners', 'update', 'url']),
                        f'&a&lhttps://github.com/{repo}', ''
                    )

                    time.sleep(10)
                    sys.exit()

            else:
                # Show the banner indicating no updates were found.
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'notFound']),
                    '', '', ''
                )

                time.sleep(2)

        except KeyboardInterrupt:
            return

    @staticmethod
    def perform_update():
        """
        Executes the automatic update of MCPTool files.
        Tries to run 'git pull' if it is a git repository with an origin remote.
        Otherwise, downloads the latest zip from GitHub repository, extracts it,
        and overwrites local files (excluding config/config.json).
        """
        repo = JsonManager.get('githubRepository') or 'wrrulos/MCPTool'
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aIniciando atualização automática...')

        # 1. Try Git Pull first
        if os.path.exists('.git'):
            try:
                # Check if a remote is configured
                remotes = subprocess.check_output('git remote', shell=True).decode().strip()
                if remotes:
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aExecutando "git pull"...')
                    res = subprocess.run('git pull', shell=True, capture_output=True)
                    if res.returncode == 0:
                        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aAtualização via Git concluída!')
                        return True
                    else:
                        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cGit pull falhou, tentando via download do ZIP...')
            except Exception:
                pass

        # 2. Download ZIP fallback
        try:
            zip_url = f'https://github.com/{repo}/archive/refs/heads/main.zip'
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aBaixando ZIP de atualização de {zip_url}...')
            
            temp_folder = 'mcptool_update_temp'
            os.makedirs(temp_folder, exist_ok=True)
            zip_path = os.path.join(temp_folder, 'update.zip')
            
            # Download file
            response = requests.get(zip_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extract zip
            extract_path = os.path.join(temp_folder, 'extracted')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Find the root folder in zip (typically 'MCPTool-main' or similar)
            subdirs = os.listdir(extract_path)
            if not subdirs:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cErro: ZIP extraído está vazio.')
                return False
                
            source_dir = os.path.join(extract_path, subdirs[0])
            
            # Overwrite files recursively (except config/config.json)
            for root, dirs, files in os.walk(source_dir):
                # Calculate relative path
                rel_path = os.path.relpath(root, source_dir)
                if rel_path == '.':
                    dest_dir = '.'
                else:
                    dest_dir = os.path.join('.', rel_path)
                    os.makedirs(dest_dir, exist_ok=True)
                
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_dir, file)
                    
                    # Skip config/config.json to prevent overwriting user options/keys
                    if os.path.normpath(dest_file) == os.path.normpath('./config/config.json'):
                        continue
                        
                    try:
                        if os.path.exists(dest_file):
                            os.remove(dest_file)
                        shutil.copy2(src_file, dest_file)
                    except Exception:
                        pass
            
            # Cleanup temp directory
            shutil.rmtree(temp_folder, ignore_errors=True)
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aAtualização via ZIP concluída com sucesso!')
            return True
            
        except Exception as e:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cErro ao realizar atualização automática: {e}')
            return False

    @staticmethod
    def check_update():
        """
        Check for updates by comparing the current and latest version numbers.

        This method retrieves the current version from JsonManager and the latest version
        from the MCPToolUpdater.get_latest_version() method. If these versions are different,
        it returns True, indicating that an update is available. Otherwise, it returns False.

        Returns:
            bool: True if an update is available, False otherwise.
        """
    
        # Get the current version from JsonManager.
        current_version = JsonManager.get('currentVersion')

        # Get the latest version from an external source (MCPToolUpdater.get_latest_version()).
        latest_version = MCPToolUpdater.get_latest_version()
        
        # Compare the current and latest versions.
        if current_version != latest_version:
            return True
        
        # No update available.
        return False

    @staticmethod
    def get_latest_version():
        """
        Retrieve the latest version of MCPTool from a remote configuration file.

        This method sends an HTTP GET request to a specific URL, which contains a JSON
        configuration file with version information. It then parses the JSON response
        and extracts the 'currentVersion' field, which represents the latest version.
        
        Returns:
            str: The latest version number as a string.
        """

        repo = JsonManager.get('githubRepository')
        if not repo or repo == 'wrrulos/MCPTool':
            # Skip checking or return current if pointing to the deleted original repo
            return JsonManager.get('currentVersion')

        try:
            # Send an HTTP GET request to the remote configuration file URL.
            response = requests.get(f'https://raw.githubusercontent.com/{repo}/main/config/config.json', timeout=10)
            if response.status_code == 200:
                js = json.loads(response.text)
                return js.get('currentVersion', JsonManager.get('currentVersion'))
        except Exception:
            pass

        return JsonManager.get('currentVersion')