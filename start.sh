#!/bin/bash

create_virtual_env() {
    # Create a virtual environment in a subdirectory of the project
    venv_dir="$(pwd)/env"
    if [ ! -d "$venv_dir" ]; then
        if python3 -m venv "$venv_dir"; then
            echo "Virtual environment created successfully."
        else
            echo "Error creating virtual environment."
            exit 1
        fi
    fi
}

install_dependencies() {
    # Install the required packages from the requirements.txt file
    if "$venv_dir/bin/python" -m pip install -r requirements.txt; then
        echo "Dependencies installed successfully."
    else
        echo "Error installing dependencies."
        exit 1
    fi
}

# Create the virtual environment
create_virtual_env

# Activate the virtual environment
source "$venv_dir/bin/activate"

# Install the required packages
install_dependencies

# Run PoeTelegramBot.py within the virtual environment
python PoeTelegramBot.py

# Deactivate the virtual environment
deactivate
