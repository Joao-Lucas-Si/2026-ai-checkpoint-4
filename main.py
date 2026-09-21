import os
import sys

import dotenv
dotenv.load_dotenv()

from src.context_rot import context_rot
from time import sleep

from rich.console import Console
from rich.progress import Progress

from rich.theme import Theme

from src.ui.screens.history_screen import HistoruScreen
# from src.ui.screens.response_screen import ResponseScreen

# from io import StringIO

def main():
    console = Console(theme=Theme({
        "background_color": "#191A1B",
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
}), )
    
    if len(sys.argv) == 2 and sys.argv[1] == "-rot":
        context_rot(console)
    else:
        HistoruScreen().draw(console)
    

if __name__ == "__main__":
    main()
