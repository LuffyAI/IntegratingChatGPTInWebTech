# Authors: Larnell Moore
# Creation Date: Jan 15, 2024
# Date Modified: Jan 15, 2024
# Purpose: This file automatically installs the program's dependencies in Ubuntu. You must run sudo python3 install.py for it work.
import subprocess
from collections.abc import Iterable
import sys
import nltk

def install_vader_lexicon():
    nltk.downloader.download('vader_lexicon')

def install_ubuntu_packages(ubuntu_packages):
    try:
        # Update Ubuntu packages
        subprocess.check_call(['sudo', 'apt-get', 'update'])
        
        #Install ubuntu packages
        for package in ubuntu_packages:
         subprocess.check_call(['sudo', 'apt-get', 'install', '-y'] + package.split())
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    else:
         print("Ubuntu packages installation completed successfully")
        
def install_python_requirements(requirements_file):
    try:
       # Install Python packages from requirements.txt
       subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    else:
         print("Python packages installation completed successfully")
         
if __name__ == "__main__":
    # List of Ubuntu packages to install
     ubuntu_packages = [
        'php=2:8.1+92ubuntu1',
        'php-cli=2:8.1+92ubuntu1',
        'php-fpm=2:8.1+92ubuntu1',
        'php-json=2:8.1+92ubuntu1',
        'php-common=2:92ubuntu1',
        'php-mysql=2:8.1+92ubuntu1',
        'php-zip=2:8.1+92ubuntu1',
        'php-gd=2:8.1+92ubuntu1',
        'php-mbstring=2:8.1+92ubuntu1',
        'php-curl=2:8.1+92ubuntu1',
        'php-xml=2:8.1+92ubuntu1',
        'php-pear=1:1.10.12+submodules+notgz+20210212-1ubuntu3',
        'php-bcmath=2:8.1+92ubuntu1',
        'php-json=2:8.1+92ubuntu1',
        'php-codesniffer=3.6.2-1'
    ]
     # Path to your requirements.txt file
     requirements_file = 'requirements.txt'

     install_ubuntu_packages(ubuntu_packages)
     install_python_requirements(requirements_file)
     install_vader_lexicon()