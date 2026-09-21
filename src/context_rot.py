import random

from prompt_toolkit.validation import ValidationError, Validator
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Column

from src.chain import main_pipeline, pipeline
from src.ui.screens.history_screen import Session


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of first non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(
                message="apenas numeros são validos", cursor_position=i
            )


def context_rot(console: Console):
    session = Session.get_session("rot")

    message = session.prompt("digite sua mensagem: ")

    # tokens = session.prompt("digite o numero máximo de tokens: ", validator=NumberValidator())

    languages = [
        "francês",
        "mandarim",
        "coreano",
        "tailandês",
        "holandês",
        "estoniano",
        "húngaro",
        "finlandês",
        "swahili",
        "turco",
        "russo",
        "guarani",
    ]

    languages_copy = languages.copy()
    with console.status("testando mémoria da ia", ) as status:
        console.print("pedindo um resumo do texto enviado")
        main_pipeline("resuma: " + message)
        
        console.print("começando testes de tradução")
        for i in range(len(languages)):
            target = languages_copy.pop(random.randint(0, len(languages_copy) - 1))
            console.print(f"pedindo tradução para o idioma {target}")

            main_pipeline(f"traduza para {target}")

    console.print("perguntando para a ia sobre quais idiomas o texto foi traduzido")
    
    languageTest = main_pipeline("quais idiomas traduzimos até agora?").lower()

    resposta = Panel(
        Markdown(languageTest),
        title="resposta da pergunta",
        subtitle="chatbot",
        border_style="#FFB71B",
    )
    console.print(resposta)

    active_languages: list[str] = []
    for language in languages:
        if language in languageTest:
            active_languages.append(language)
    relatorio = Panel(
        f"de todos os idiomas requeridos uma tradução, sendo eles: {", ".join(languages)}, \napenas estes foram lembrados: {", ".join(active_languages)}"
        + "\n"
        + f"assim, totalizando {len(active_languages)} idiomas lembrados de {len(languages)} idiomas, com {len(languages) - len(active_languages)} sendo esquecidos",
        title="Relatorio",
        border_style="#93358D",
    )
    console.print(relatorio)
