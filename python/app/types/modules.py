from dataclasses import dataclass


@dataclass
class Module:
    key: str
    title: str

    def __str__(self):
        return f"Module {self.key}: {self.title}"
