import click
import textwrap

from pathlib import Path

from app import scenarios
from app.utils import exit_on_error, get_user_input, run_cli


def loop(scenario_id: str):
    scenario = scenarios.get(scenario_id)

    func = scenario.function
    extra_args = scenario.args

    click.echo(f"\n{scenario.description}")
    root_path = Path(__file__).parent.absolute()
    click.echo(f"Code location: {root_path / scenario.file_location}\n")

    while True:
        user_input = get_user_input().strip()
        if user_input == "/x":
            break
        response = func(user_input, *extra_args)
        if "error" in response:
            exit_on_error(response["error"])

        wrapped_response = textwrap.fill(response["response_text"].strip(), width=120)
        click.echo(f"{wrapped_response}\n")

        if "conversation" in response:
            extra_args = (*extra_args, response["conversation"])


if __name__ == '__main__':
    app = run_cli(loop, scenarios)
    app()
