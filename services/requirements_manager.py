import os.path
import shutil

from .custom_logger import CustomLogger


def copy_requirements(base_dir: str, requirements_file: str, logger: CustomLogger) -> None:
    # Destination path for the requirements file inside the docker addons folder
    destination = os.path.join(base_dir, 'addons', 'requirements.txt')

    # Create an empty requirements file if it doesn't exist in the provided addons folder
    if requirements_file != './addons/requirements.txt' and not os.path.exists(requirements_file):
        logger.print_warning(f"Requirements file not found at {requirements_file}, creating an empty file")
        with open(requirements_file, 'w') as f:
            f.write("")
        logger.print_success(f"Successfully created empty requirements file at {requirements_file}")

    # Copy the requirements file from the provided addons folder to the docker addons folder
    if requirements_file != './addons/requirements.txt':
        shutil.copyfile(requirements_file, destination)

    # Create an empty requirements file if it doesn't exist in the docker addons folder
    if not os.path.exists(destination):
        logger.print_warning(f"Requirements file not found, creating an empty file")
        with open(destination, 'w') as f:
            f.write("")
        logger.print_success(f"Successfully created empty requirements file")
