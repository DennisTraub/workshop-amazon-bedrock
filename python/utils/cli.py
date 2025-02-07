import click


def run_cli(loop, scenarios):
    @click.group()
    def app():
        pass

    @app.command(name="run")
    @click.argument("scenario", required=False, type=click.Choice(list(scenarios.keys())))
    def run_scenario(scenario: str):
        """Runs a specified scenario"""
        if scenario:
            loop(scenario)
        else:
            print_missing_scenario_message(scenarios)

    @app.command(name="list")
    def list_scenarios():
        """Lists all scenarios"""
        print_scenarios(scenarios, with_modules=True)

    return app

def print_missing_scenario_message(scenarios):
    available_scenario_numbers = "'{" + "|".join(list(scenarios.keys())) + "}'"
    click.echo(f"Usage: app.py run [OPTIONS] {available_scenario_numbers}")
    click.echo("Try 'app.py run --help' for help.\n")
    click.echo(f"Error: Missing scenario number {available_scenario_numbers}. Choose from:\n")
    print_scenarios(scenarios)

def print_scenarios(scenarios, with_modules=False):
    current_module = None
    for scenario_id, scenario in scenarios.items():
        if scenario["module"] != current_module:
            current_module = scenario["module"]
            if with_modules:
                click.echo(f"\nModule: {current_module}")

        click.echo(f"{scenario_id} - {scenario["description"]}")

def exit_on_error(err: Exception):
    if err:
        print(f"Error: {err}")
        exit(1)
