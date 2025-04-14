import click
import os
import re

from app.config import vector_db_folder
from app.utils.vector_db import initialize_vector_db


def parse_scenario_input(input_str: str, available_scenarios: list) -> list:
    """
    Parse a string of scenarios into a list of scenario IDs.
    Supports comma-separated lists and ranges (e.g. "1,3,5-8").
    """
    if not input_str:
        return []
    
    # Split by commas and process each part
    parts = input_str.split(',')
    scenarios = set()
    
    for part in parts:
        part = part.strip()
        # Check for range format (e.g. "5-8")
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start > end:
                start, end = end, start
            scenarios.update(str(i) for i in range(start, end + 1))
        else:
            scenarios.add(part)
    
    # Filter out invalid scenarios
    valid_scenarios = [s for s in scenarios if s in available_scenarios]
    return sorted(valid_scenarios, key=int)


def run_cli(loop, scenarios):
    @click.group()
    def app():
        pass

    @app.command(name="run")
    @click.argument("scenario_input", required=False, nargs=-1)
    def run_scenario(scenario_input):
        """Runs one or more scenarios. Examples:
        - app.py run 1        # Run scenario 1
        - app.py run 1,3,5    # Run scenarios 1, 3, and 5
        - app.py run 5-8      # Run scenarios 5 through 8
        - app.py run 1,3,5-8  # Run scenarios 1, 3, and 5 through 8
        """
        available_scenarios = list(scenarios.keys())
        
        if not scenario_input:
            print_missing_scenario_message(scenarios)
            return
            
        # Join all arguments into a single string and remove any extra spaces
        scenario_str = ' '.join(scenario_input).replace(' ', '')
        
        # Parse the input into a list of scenario IDs
        scenario_ids = parse_scenario_input(scenario_str, available_scenarios)
        
        if not scenario_ids:
            click.echo(f"Error: No valid scenarios found in input. Available scenarios: {', '.join(available_scenarios)}")
            return
            
        # Initialize vector DB if needed
        if "9" in scenario_ids and not os.path.exists(vector_db_folder):
            click.echo("Initializing vector database...")
            initialize_vector_db()
            
        # Run each scenario
        for scenario_id in scenario_ids:
            loop(scenario_id, scenarios)

    @app.command(name="list")
    def list_scenarios():
        """Lists all scenarios"""
        print_scenarios(scenarios)

    return app

def print_missing_scenario_message(scenarios):
    available_scenario_numbers = scenarios.format_available_scenario_numbers()
    click.echo(f"Usage: app.py run [OPTIONS] [SCENARIO_INPUT]")
    click.echo("Examples:")
    click.echo("  app.py run 1              # Run scenario 1")
    click.echo("  app.py run 1,3,5          # Run scenarios 1, 3, and 5")
    click.echo("  app.py run 5-8            # Run scenarios 5 through 8")
    click.echo("  app.py run 1,3,5-8        # Run scenarios 1, 3, and 5 through 8")
    click.echo("\nTry 'app.py run --help' for help.\n")
    click.echo(f"Available scenarios: {available_scenario_numbers}\n")
    print_scenarios(scenarios)

def print_scenarios(scenarios):
    click.echo(scenarios)

def exit_on_error(err: Exception):
    if err:
        print(f"Error: {err}")
        exit(1)
