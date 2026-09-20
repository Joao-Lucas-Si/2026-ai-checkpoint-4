import dotenv
dotenv.load_dotenv()
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
    steps = [
        "classificando tarefa",
        "gerando resposta",
    ]

    # with console.status("gerando resposta") as status:
    #     # with Progress() as progress:
    #     length = len(steps)
    #         # task = progress.add_task("respondendo...", total=length)
    #         # current= 0
    #     while steps:
    #         sleep(1)
    #         # current+=1
    #         # progress.update(task , advance= 1)
    #         step = steps.pop(0)
    #         console.log(step)
    HistoruScreen().draw(console)
    # ResponseScreen().draw(console)


if __name__ == "__main__":
    main()
