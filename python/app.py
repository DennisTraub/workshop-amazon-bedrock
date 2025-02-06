import click
import textwrap

from config import scenarios
from utils import exit_on_error, get_user_input, run_cli


def loop(scenario_id: str):
    scenario_config = scenarios.get(scenario_id)

    func = scenario_config.get("function")
    extra_args = scenario_config.get("args", [])

    while True:
        user_input = get_user_input()
        if user_input == "/x":
            break

        response, err = func(user_input, *extra_args)
        exit_on_error(err)

        wrapped_response = textwrap.fill(response.strip(), width=120)
        click.echo(f"{wrapped_response}\n")

if __name__ == '__main__':
    app = run_cli(loop, scenarios)
    app()
