from typing import Literal, Union

from pydantic import BaseModel, ConfigDict




class AnaliseSchema(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    
    tipo: Literal["resumo","expansao","brainstorm"]
    "o tipo da tarefa requerida"
    tema: str
    "o tema do texto"
    palavras_chaves: list[str]
    "palavras chaves importantes que devem ser lembrados"
    tipo_descrita: list[str]
    "o tipo de descrita requisitada ou interferida"


# class AnaliseResposta(BaseModel):
#     model_config = ConfigDict(use_attribute_docstrings=True)
#     tipo: RespostaTipo
#     tema: RespostaTema
#     intencao_principal: str
#     palavras_chaves: list[str]
#     resumo: str

# class Recomendacao(BaseModel):
#     model_config = ConfigDict(use_attribute_docstrings=True)
#     nome: str
#     """nome do posto ou número do carregador"""
#     motivo: str
#     "motivo da escolha"

# class AnalisePostos(BaseModel):
#     model_config = ConfigDict(use_attribute_docstrings=True)
#     recomendados: list[Recomendacao]
#     """lista dos postos ou carregadores recomendados"""
#     nao_recomendados: list[Recomendacao]
#     """lista de postos ou carregadores não recomendados"""
#     relatorio_geral: str
#     """resumo geral sobre a situação dos postos"""
