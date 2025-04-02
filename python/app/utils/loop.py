import click
import textwrap
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
import inspect

from app.utils import exit_on_error, get_user_input
from app.utils.editor import edit_code

# Create a rich console for rendering markdown
console = Console()

def get_scenario_explanation(scenario_id, scenario):
    """
    Get the explanation for a scenario from its markdown file.
    Returns an empty string if the file doesn't exist.
    """
    # Get the source file path
    source_file = scenario.load_source_code()
    if not source_file:
        return ""
    
    # Get the source file path from the scenario
    source_path = None
    try:
        # Try to get the source file path from the scenario function
        source_path = inspect.getsourcefile(scenario.function)
    except Exception:
        # If that fails, try to find the file based on the scenario ID
        for module_dir in ["module_1", "module_2", "module_3"]:
            potential_path = Path.cwd() / module_dir / f"scenario_{scenario_id}_*.py"
            matching_files = list(Path.cwd().glob(str(potential_path)))
            if matching_files:
                source_path = matching_files[0]
                break
    
    if not source_path:
        return ""
    
    # Construct the path to the markdown file
    markdown_path = Path(source_path).with_suffix('.md')
    
    # Check if the markdown file exists
    if not markdown_path.exists():
        return ""
    
    # Read the markdown file
    try:
        with open(markdown_path, 'r') as f:
            return f.read()
    except Exception as e:
        click.echo(f"Error reading markdown file: {e}")
        return ""

def loop(scenario_id, scenarios):
    is_first_message = True
    scenario = scenarios.get(scenario_id)

    func = scenario.function
    extra_args = scenario.args

    click.echo(f"\n{scenario}")
    click.echo("=" * 68)
    
    # Show the explanation for the scenario
    explanation = get_scenario_explanation(scenario_id, scenario)
    if explanation:
        # Render the markdown content using rich
        console.print(Markdown(explanation))
        click.echo("\nPress Enter to continue to the code editor...")
        input()
    
    # Show the source code of the scenario
    source_code = scenario.load_source_code()
    if source_code:
        click.echo("\nOpening code editor...")
        edited_code = edit_code(source_code)
        if edited_code != source_code:
            click.echo("\nRunning edited code...")
            def execute_edited(user_input, *args):
                return scenario.execute_edited_code(edited_code, user_input, *args)
            func = execute_edited
        else:
            click.echo("\nRunning original code...")
            click.echo()  # Add an empty line for better readability
    
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
