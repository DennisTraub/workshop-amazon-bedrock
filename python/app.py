import boto3

from utils import exit_on_error
from utils.cli import run_cli
from utils.input import get_user_input
from bedrock.bedrock import invoke_model


def loop(session: boto3.Session):
    while True:
        user_input = get_user_input()

        if user_input == "/x":
            break

        response, err = invoke_model(user_input, session)
        exit_on_error(err)

        print(response)

if __name__ == '__main__':
    app = run_cli(loop)
    app()
