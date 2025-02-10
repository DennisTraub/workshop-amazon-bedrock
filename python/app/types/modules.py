from dataclasses import dataclass
from typing import List


@dataclass
class Module:
    key: str
    title: str

    def __str__(self):
        return f"Module {self.key}: {self.title}"


@dataclass
class Modules:
    _modules: List[Module]

    def get(self, key: str):
        return next((m for m in self._modules if m.key == key), None)
