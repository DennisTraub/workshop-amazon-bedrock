from dataclasses import dataclass, field
from typing import Callable, List

from . import Module


@dataclass
class Scenario:
    id: str
    module: Module
    title: str
    function: Callable
    args: List[str] = field(default_factory=list)

    def __str__(self):
        return (
            f"{self.module}\n"
            f"Scenario {self.id}: {self.title}"
        )


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
