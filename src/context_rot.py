import random

from prompt_toolkit.validation import ValidationError, Validator
from rich.console import Console

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
                message="apenas numeros são validos",
                cursor_position=i
            )

def context_rot(console: Console):
    session = Session.get_session("rot")

    message=  session.prompt("digite sua mensagem: ")

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
        "guarani"
    ]

    

    main_pipeline("resuma: " + message)

    languages_copy = languages.copy()

    for i in range(len(languages)):
        target = languages_copy.pop(random.randint(0, len(languages_copy) - 1))

        main_pipeline(f"traduza para {target}")

    languageTest = main_pipeline("quais idiomas traduzimos até agora?").lower()


    print(languageTest)

    active_languages: list[str] = []
    for language in languages:
        if language in languageTest:
            active_languages.append(language)
    console.print("")
    console.print(f"de todos os idiomas requeridos uma tradução, sendo eles: {", ".join(languages)}, apenas estes foram lembrados: {", ".join(active_languages)}")
    console.print(f"assim, totalizando {len(active_languages)} idiomas lembrados de {len(languages)} idiomas, com {len(languages) - len(active_languages)} sendo esquecidos")