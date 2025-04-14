from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any
import inspect
import os
import tempfile
import importlib.util
import sys

from . import Module


@dataclass
class Scenario:
    id: str
    module: Module
    title: str
    function: Callable
    args: List[str] = field(default_factory=list)
    source_code: str = field(default="")

    def __str__(self):
        return (
            f"{self.module}\n"
            f"Scenario {self.id}: {self.title}"
        )

    def load_source_code(self):
        """Load the source code of the scenario function"""
        if not self.source_code:
            # Get the source file path
            source_file = inspect.getsourcefile(self.function)
            if source_file:
                # Read the file content
                with open(source_file, 'r') as f:
                    self.source_code = f.read()
        return self.source_code

    def execute_edited_code(self, edited_code: str, user_input: str, *args) -> Dict[str, Any]:
        """
        Execute the edited code in a temporary file and return the result.
        This is safer than using eval() as it provides proper isolation.
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(edited_code)
            temp_file = f.name

        try:
            # Import the temporary module
            spec = importlib.util.spec_from_file_location("temp_module", temp_file)
            if not spec or not spec.loader:
                raise ImportError("Could not load the edited code")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules["temp_module"] = module
            spec.loader.exec_module(module)

            # Find the main function (should be the first function in the file)
            main_func = None
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    main_func = obj
                    break

            if not main_func:
                raise ValueError("No main function found in the edited code")

            # Execute the function
            return main_func(user_input, *args)

        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file)
            except:
                pass


@dataclass
class Scenarios:
    _scenarios: List[Scenario]

    def __iter__(self):
        return iter(self._scenarios)

    def __str__(self):
        result: str = ""
        current_module = None
        for scenario in self._scenarios:
            if scenario.module != current_module:
                current_module = scenario.module
                result += f"\n{current_module}\n"
                result += ("=" * 68) + "\n"
            result += f"{scenario.id} - {scenario.title}\n"

        return result

    def keys(self):
        return [s.id for s in self._scenarios]

    def get(self, key: str):
        return next((s for s in self._scenarios if s.id == key), None)

    def format_available_scenario_numbers(self, delimiter="|"):
        return delimiter.join(list(self.keys()))
