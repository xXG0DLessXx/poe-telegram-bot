import os
import platform
import subprocess
import sys
from setuptools import find_packages, setup

def create_virtual_env():
    """Create a virtual environment in a subdirectory of the project."""
    venv_dir = os.path.join(os.getcwd(), 'env')
    if not os.path.exists(venv_dir):
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
        except subprocess.CalledProcessError as e:
            print('Error creating virtual environment:', e)
            sys.exit(1)

def install_dependencies():
    """Install the required packages from the requirements.txt file."""
    try:
        subprocess.check_call([os.path.join('env', 'bin', 'pip'), 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError as e:
        print('Error installing dependencies:', e)
        sys.exit(1)

if __name__ == '__main__':
    # Create the virtual environment
    create_virtual_env()

    # Install the required packages
    install_dependencies()

    # Run PoeTelegramBot.py within the virtual environment
    subprocess.check_call([os.path.join('env', 'bin', 'python'), 'PoeTelegramBot.py'])