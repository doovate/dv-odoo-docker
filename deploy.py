import typer
import asyncio
import os
import sys
import time
from dotenv import load_dotenv

from services.custom_logger import CustomLogger
from services.startup_validator import env_verify
from services.commands import Commands
from services.config_manager import set_config
from services.requirements_manager import copy_requirements

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
app = typer.Typer(add_completion=False,
                  help="Odoo Deploy command line tool, run without arguments nor commands to start the deployment process")
base_dir = os.path.dirname(os.path.abspath(__file__))
logger = CustomLogger("odoo_deploy")


async def async_main():
    start_time = time.time()
    load_dotenv()

    env_variables = {
        'VERSION': os.getenv('VERSION'),
        'TRAEFIK_VERSION': os.getenv('TRAEFIK_VERSION'),
        'COMPOSE_PROJECT_NAME': os.getenv('COMPOSE_PROJECT_NAME'),
        'DEPLOYMENT_TARGET': os.getenv('DEPLOYMENT_TARGET'),
        'ODOO_VERSION': os.getenv('ODOO_VERSION'),
        'POSTGRES_VERSION': os.getenv('POSTGRES_VERSION'),
        'ODOO_EXPOSED_PORT': os.getenv('ODOO_EXPOSED_PORT'),
        'ODOO_INTERNAL_PORT': os.getenv('ODOO_INTERNAL_PORT'),
        'ODOO_LOG': os.getenv('ODOO_LOG'),
        'ODOO_CONFIG': os.getenv('ODOO_CONFIG'),
        'ODOO_ADDONS': os.getenv('ODOO_ADDONS'),
        'DOMAIN': os.getenv('DOMAIN'),
        'OPTIONAL_WHISPER': os.getenv('OPTIONAL_WHISPER'),
        'AUTO_INSTALL_MODULES': os.getenv('AUTO_INSTALL_MODULES'),
        'AUTO_UPDATE_MODULES': os.getenv('AUTO_UPDATE_MODULES'),
        'UPDATE_MODULE_LIST': os.getenv('UPDATE_MODULE_LIST'),
        'FORCE_UPDATE': os.getenv('FORCE_UPDATE'),
        'FORCE_REBUILD': os.getenv('FORCE_REBUILD'),
    }

    # Verify environment variables
    env_verify(env_variables=env_variables, logger=logger)

    # Copy the requirements file to the addons folder
    copy_requirements(
        base_dir=base_dir,
        requirements_file=os.path.join(env_variables['ODOO_ADDONS'], 'requirements.txt'),
        logger=logger
    )

    commands = Commands(logger=logger, environment=env_variables)

    await commands.start_containers()

    end_time = time.time() - start_time
    logger.print_success(f"Total time: {end_time:.2f} seconds")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """ Launch and configure Odoo and PostgresSQL containers """
    if not ctx.invoked_subcommand:
        asyncio.run(async_main())


@app.command()
def auto_config():
    """ Autoconfigure Odoo and PostgresSQL config files based on server capacity"""
    set_config(
        base_dir=base_dir,
        logger=logger
    )


# Entry point
if __name__ == "__main__":
    app()
