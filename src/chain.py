import sys
from typing import TypeVar, overload

from langchain.chat_models import init_chat_model
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.utils.pydantic import PydanticBaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel

from src.schemas import AnaliseSchema
from src.memory import TokenMemory 

model = ChatOllama(
    model="gemma4:cloud",
    base_url="https://ollama.com",
    
)
memory = TokenMemory()

T = TypeVar("T",  bound=BaseModel)

@overload
def pipeline(system: str, message: str, format: type[T], *, persona: str = "",  data: dict = {}) -> T: ...

@overload
def pipeline(system: str, message: str, *, persona: str= "",  data: dict = {}) -> str: ...

def pipeline(system: str, message: str, format: type[BaseModel]|None = None, *, data: dict = {}, persona: str = "assets/prompt/main/persona.md") -> str|T:
    
    base = open("assets/prompt/templates/base.md").read()
    # return base

    prompt = ChatPromptTemplate(messages=[
        ("system", base),
        # MessagesPlaceholder("history"),
        *memory.chat_message(),
        ("human", message)
    ])
    llm: Runnable = model
    if format:
        # model.output_schema
        # llm = model.with_structured_output(format)
        model.format = "json"
    else:
        model.format = None

    # return prompt.format_messages(**{
    #     "objetivo": open(f"assets/prompt/main/{system}/{system}-objetivo.md").read(),
    #     "regras": open(f"assets/prompt/main/{system}/{system}-regras.md").read(),
    #     "persona": open(f"assets/prompt/main/persona.md").read()
    # })[-1].text
    # return ""
    # memory.save_context(inputs={}, outputs={})
    
    # return sys.argv[1]])
    # message = model.invoke(sys.argv[1])
    parser = ( PydanticOutputParser(pydantic_object= format) if format  else StrOutputParser())
    prompt = prompt.partial(format_instructions= "siga esse formato para o json: \n" + parser.get_format_instructions().replace("{", "\\{{").replace("}", "\\}}") if isinstance(parser, PydanticOutputParser) else "" )
    chain = prompt  | llm | parser



    response: str|T = chain.invoke({
        "tipo": "",
        "objetivo": open(f"assets/prompt/main/{system}/{system}-objetivo.md").read(),
        "regras": open(f"assets/prompt/main/{system}/{system}-regras.md").read(),
        "persona": open(persona).read(),
        "input": message
    } | data)

    memory.save_context('human', prompt.format(**{
        "tipo": "",
        "objetivo": open(f"assets/prompt/main/{system}/{system}-objetivo.md").read(),
        "regras": open(f"assets/prompt/main/{system}/{system}-regras.md").read(),
        "persona": open(persona).read(),
        "input": message
    } | data)[-1])
    memory.save_context("ai",  response.model_dump_json().replace("{", "\\{{").replace("}", "\\}}") if isinstance(response, BaseModel) else response)
    
    return response


def main_pipeline(prompt: str, ):
    analise = pipeline("analise", prompt,format=AnaliseSchema, persona="assets/prompt/main/analise/analise-persona.md")
    
    response = pipeline(analise.tipo, f"""
[analise]
{str(analise)}
[input do usuario]
{{prompt}}
    """, data={
        "prompt": prompt,
        # "analise": str(analise)
    })

    return response