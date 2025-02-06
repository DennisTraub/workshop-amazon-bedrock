import click

from utils.aws import try_initialize_session

def run_cli(loop):
    @click.group()
    def app():
        pass

    @app.command()
    @click.option("--region", '-r', default=None, help="The AWS Region")
    def run(region):
        session, err = try_initialize_session(region)
        if err:
            print(f"Error: {err}")
            exit(1)

        loop(session)

    return app

def exit_on_error(err: Exception):
    if err:
        print(f"Error: {err}")
        exit(1)
