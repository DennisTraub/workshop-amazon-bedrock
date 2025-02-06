import click
import textwrap

from bedrock import (
    invoke_model,
    invoke_llama,
    invoke_llama_with_chat_template
)

from utils import (
    exit_on_error,
    run_cli,
    get_user_input
)

scenarios = {
    "1": {
        "function": invoke_model,
        "description": "Invoke Claude 3.5 Haiku"
    },
    "2": {
        "function": invoke_llama,
        "description": "Invoke Llama 3.1 without Meta's chat template"
    },
    "3": {
        "function": invoke_llama_with_chat_template,
        "description": "Invoke LLama 3.1 with Meta's chat template"
    },
}

def loop(scenario: str):
    while True:
        user_input = get_user_input()

        if user_input == "/x":
            break

        func = scenarios.get(scenario).get("function")
        if not func:
            raise ValueError(f"Invalid scenario: {scenario}")

        response, err = func(user_input)

        exit_on_error(err)

        wrapped_response = textwrap.fill(response.strip(), width=120)

        click.echo(f"{wrapped_response}\n")

if __name__ == '__main__':
    app = run_cli(loop, scenarios)
    app()
