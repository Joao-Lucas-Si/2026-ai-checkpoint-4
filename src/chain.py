import sys
from typing import TypeVar, overload

from langchain.chat_models import init_chat_model
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.utils.pydantic import PydanticBaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel

from src.memory import TokenMemory 

model = ChatOllama(
    model="gemma4:cloud",
    base_url="https://ollama.com",
)
memory = TokenMemory()

T = TypeVar("T",  bound=BaseModel)

@overload
def pipeline(system: str, message: str, format: type[T]) -> T: ...

@overload
def pipeline(system: str, message: str) -> str: ...

def pipeline(system: str, message: str, format: type[BaseModel]|None = None) -> str|T:
    
    base = open("assets/prompt/templates/base.md").read()
    # return base

    prompt = ChatPromptTemplate(messages=[
        ("system", base),
        # MessagesPlaceholder("history"),
        *memory.chat_message(),
        ("human", message)
    ])

    # return prompt.format_messages(**{
    #     "objetivo": open(f"assets/prompt/main/{system}/{system}-objetivo.md").read(),
    #     "regras": open(f"assets/prompt/main/{system}/{system}-regras.md").read(),
    #     "persona": open(f"assets/prompt/main/persona.md").read()
    # })[-1].text
    # return ""
    # memory.save_context(inputs={}, outputs={})
    
    # return sys.argv[1]
    # message = model.invoke(sys.argv[1])
    chain = prompt  | model | ( PydanticOutputParser(pydantic_object= format) if format  else StrOutputParser())

    response: str|T = chain.invoke({
        "objetivo": open(f"assets/prompt/main/{system}/{system}-objetivo.md").read(),
        "regras": open(f"assets/prompt/main/{system}/{system}-regras.md").read(),
        "persona": open(f"assets/prompt/main/persona.md").read(),
        "input": message
    }, {
        "configurable": {
            "session_id": "base"
        }
        # "session_id": memory.chat_memory.id
    })

    memory.save_context('human', message)
    memory.save_context("ai",  response.model_dump_json() if isinstance(response, BaseModel) else response)
    
    return response
