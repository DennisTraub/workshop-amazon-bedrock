import click

from config.scenarios import modules


def run_cli(loop, scenarios):
    @click.group()
    def app():
        pass

    @app.command(name="run")
    @click.argument("scenario",type=click.Choice(list(scenarios.keys())),)
    def run_scenario(scenario: str):
        """Runs a specified scenario"""
        loop(scenario)

    @app.command(name="list")
    def list_scenarios():
        """Lists all scenarios"""
        current_module = None

        for scenario_id, scenario in scenarios.items():
            if scenario["module"] != current_module:
                current_module = scenario["module"]
                module_id = next(k for k, v in modules.items() if v == current_module)
                click.echo(f"\nModule {module_id}: {current_module}")

            click.echo(f"Scenario {scenario_id}: {scenario["description"]}")


    return app

def exit_on_error(err: Exception):
    if err:
        print(f"Error: {err}")
        exit(1)
