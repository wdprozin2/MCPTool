import os
import re
import sys
import shutil
import zipfile
import requests
import subprocess
from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities

class SoftwareUpdater:
    @staticmethod
    def update_all_software():
        """
        Executes automatic updates for extra software components:
        - Ngrok
        - Python requirements (pip)
        - Node.js modules (npm)
        """
        try:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aVerificando atualizações de softwares auxiliares...')
            
            # Update Python dependencies
            SoftwareUpdater.update_python_dependencies()
            
            # Update Node.js dependencies
            SoftwareUpdater.update_nodejs_dependencies()
            
            # Update Ngrok (if applicable for platform)
            if os.name == 'nt' or CheckUtilities.check_termux() or sys.platform.startswith('linux'):
                SoftwareUpdater.update_ngrok()
                
        except Exception as e:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cErro ao atualizar softwares auxiliares: {e}')

    @staticmethod
    def update_python_dependencies():
        try:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aVerificando e atualizando pacotes Python...')
            cmd = f'"{sys.executable}" -m pip install -r requirements.txt --upgrade >nul 2>&1'
            subprocess.run(cmd, shell=True)
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aPacotes Python atualizados com sucesso.')
        except Exception as e:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cErro ao atualizar dependências do Python: {e}')

    @staticmethod
    def update_nodejs_dependencies():
        try:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aVerificando e atualizando módulos do Node.js...')
            cmd = 'npm install >nul 2>&1'
            subprocess.run(cmd, shell=True)
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aMódulos do Node.js atualizados com sucesso.')
        except Exception as e:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cErro ao atualizar módulos do Node.js: {e}')

    @staticmethod
    def update_ngrok():
        # Scrapes the ngrok download page for latest windows download link and updates it
        if os.name != 'nt':
            # Non-Windows platforms usually use system-wide packages or setup command install
            return
            
        try:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aVerificando atualizações do Ngrok...')
            
            response = requests.get('https://ngrok.com/download', timeout=10)
            html = response.content.decode('utf-8')
            ngrok_link_pattern = r'href=["\'](https://bin\.ngrok\.com/c/[^"\']+/ngrok-v3-stable-windows-amd64\.zip)["\']'
            match = re.search(ngrok_link_pattern, html)
            
            if match:
                download_link = match.group(1)
            else:
                download_link = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip'
                
            # Check if we already have it or need to download it
            # We can store the downloaded URL in config or just overwrite it
            # Overwriting ensures we have the latest version
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aBaixando versão mais recente do Ngrok...')
            
            zip_name = 'Ngrok_update.zip'
            with open(zip_name, 'wb') as f:
                file_data = requests.get(download_link, timeout=15)
                f.write(file_data.content)
            
            temp_dir = 'NgrokZip_temp'
            os.makedirs(temp_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_name, 'r') as archive:
                archive.extractall(temp_dir)
            
            # Copy ngrok.exe to root
            src_exe = os.path.join(temp_dir, 'ngrok.exe')
            if os.path.exists(src_exe):
                if os.path.exists('ngrok.exe'):
                    os.remove('ngrok.exe')
                shutil.copy(src_exe, 'ngrok.exe')
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&aNgrok atualizado com sucesso para a versão mais recente.')
            
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            if os.path.exists(zip_name):
                os.remove(zip_name)
                
        except Exception as e:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}&cErro ao atualizar o Ngrok: {e}')
