from app.config import scenarios
from app.utils import loop, run_cli


def main():
    app = run_cli(loop, scenarios)
    app()


if __name__ == '__main__':
    main()
