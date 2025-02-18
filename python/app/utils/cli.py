import click
import os

from app.config import vector_db_folder
from app.utils.vector_db import initialize_vector_db


def run_cli(loop, scenarios):
    @click.group()
    def app():
        pass

    @app.command(name="run")
    @click.argument("scenario", required=False, type=click.Choice(list(scenarios.keys())))
    def run_scenario(scenario: str):
        """Runs a specified scenario"""
        if scenario:
            if scenario == "9" and not os.path.exists(vector_db_folder):
                # Initialize the vector database
                click.echo("Initializing vector database...")
                initialize_vector_db()
            loop(scenario, scenarios)
        else:
            print_missing_scenario_message(scenarios)

    @app.command(name="list")
    def list_scenarios():
        """Lists all scenarios"""
        print_scenarios(scenarios)

    return app

def print_missing_scenario_message(scenarios):
    available_scenario_numbers = scenarios.format_available_scenario_numbers()
    click.echo(f"Usage: app.py run [OPTIONS] {available_scenario_numbers}")
    click.echo("Try 'app.py run --help' for help.\n")
    click.echo(f"Error: Missing scenario number {available_scenario_numbers}. Choose from:\n")
    print_scenarios(scenarios)

def print_scenarios(scenarios):
    click.echo(scenarios)

def exit_on_error(err: Exception):
    if err:
        print(f"Error: {err}")
        exit(1)
