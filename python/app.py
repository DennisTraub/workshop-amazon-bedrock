from _app.scenario_config import scenarios
from _app.utils import loop, run_cli


if __name__ == '__main__':
    app = run_cli(loop, scenarios)
    app()
