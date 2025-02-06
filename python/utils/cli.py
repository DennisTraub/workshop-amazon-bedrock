import click


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
        for key, scenario in scenarios.items():
            click.echo(f"Scenario {key}: {scenario["description"]}")

    return app

def exit_on_error(err: Exception):
    if err:
        print(f"Error: {err}")
        exit(1)
