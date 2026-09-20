from abc import ABC

from rich.console import Console


class Screen(ABC):
    def draw(self, console: Console):
        ...