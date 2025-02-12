import click
import textwrap

from app.utils import exit_on_error, get_user_input

def loop(scenario_id, scenarios):
    is_first_message = True
    scenario = scenarios.get(scenario_id)

    func = scenario.function
    extra_args = scenario.args

    click.echo(f"\n{scenario}")
    click.echo("=" * 68)

    while True:
        user_input = get_user_input().strip()
        if user_input == "/x":
            break
        response = func(user_input, *extra_args)
        if "error" in response:
            exit_on_error(response["error"])

        response_lines = textwrap.wrap(response["response_text"].strip(), width=120)
        lines = "\n".join(response_lines)
        click.echo(f"{lines}\n")

        if "conversation" in response and is_first_message:
            extra_args = (*extra_args, response["conversation"])
            is_first_message = False
