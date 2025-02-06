import click

from utils.aws import try_initialize_session
from utils.input import get_user_input


@click.group()
def app():
    pass

@app.command()
@click.option("--region", '-r', default=None, help="The AWS Region")
def run(region):
    boto3_session, err = try_initialize_session(region)
    if err:
        print(f"Error: {err}")
        exit(1)

    while True:
        user_input = get_user_input()
        if user_input == "/x":
            break
        print("Hi\n")

if __name__ == '__main__':
    app()
