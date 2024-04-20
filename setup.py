import os
import sys
import subprocess


def create_venv(directory: str):
    """
    Creates a virtual environment and installs requirements for a given directory
    """
    # Create venv path within the directory
    venv_path = os.path.join(directory, ".venv")

    # Create new venv if one doesn't exist
    if not os.path.exists(venv_path):
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print(f"Virtual environment created for {directory}")

    # Update pip
    venv = os.path.join(venv_path, "Scripts", "python")
    subprocess.run([venv, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    return venv_path


def install_requirements(venv_path: str, directory: str):
    """
    Install all requirements for directory (using pip)
    """
    pip = os.path.join(venv_path, "Scripts", "pip")
    requirements_file = os.path.join(directory, "requirements.txt")

    if os.path.exists(requirements_file):
        subprocess.run([pip, "install", "-r", requirements_file], check=True)
        print(f"Installed requirements from {requirements_file} for {directory}")

    else:
        print(f"No requirements.txt found in {directory}")

    # Install Physics Exercise Helpers
    subprocess.run([pip, "install", "-e", "helpers"], check=True)
    print(f"Installed Physics Exercise Helpers")


# Verify Python version
assert sys.version_info >= (3, 10)

# Get all directories under the current directory
top_level_directories = [
    "Second Year",
    "Third Year",
]

for directory in top_level_directories:

    # Check if directory exists
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' not found.")
        continue

    # Get all subdirectories within the target directory
    subdirectories = [
        os.path.join(directory, subdir)
        for subdir in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, subdir))
    ]

    # Create venv and install requirements for each subdirectory
    for subdir in subdirectories:
        venv = create_venv(subdir)
        install_requirements(venv, subdir)
