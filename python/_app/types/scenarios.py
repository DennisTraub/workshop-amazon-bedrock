from dataclasses import dataclass, field
from typing import Callable, List

from . import Module


@dataclass
class Scenario:
    key: str
    module: Module
    title: str
    function: Callable
    args: List[str] = field(default_factory=list)
    description: str = ""
    file_location: str = ""


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
                result += ("=" * 52) + "\n"
            result += f"{scenario.key} - {scenario.title}\n"

        return result

    def keys(self):
        return [s.key for s in self._scenarios]

    def get(self, key: str):
        return next((s for s in self._scenarios if s.key == key), None)

    def format_available_scenario_numbers(self, delimiter="|"):
        return delimiter.join(list(self.keys()))
