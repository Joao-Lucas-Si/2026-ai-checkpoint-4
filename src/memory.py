from abc import ABC
from typing import Any, Literal
import tiktoken

from langchain_core.messages import BaseMessage, MessageLikeRepresentation


def contar_tokens(texto):
    encoding = tiktoken.get_encoding("o200k_base")
 
    return len(encoding.encode(texto))

class Message():
    tokens: int
    content: str
    type: Literal["ai","human"]

    def __init__(self, tokens: int, content: str, type: Literal["ai","human"]) -> None:
        self.tokens = tokens
        self.content = content
        self.type = type

class Memory(ABC):
    messages: list[Message] = []

    def chat_message(self) -> list[tuple[str, str | list[str | dict[str, Any]]]]:
        return [(message.type, message.content) for message in self.messages]

    def save_context(self, type: Literal["ai", "human"], message: str):
        ...

class TokenMemory(Memory):
    max_tokens = 1000
    def save_context(self, type: Literal["ai", "human"], message: str):
        tokens = contar_tokens(message)
        
        self.messages.append(Message(tokens, message, type))
        
        def calc_tokens():
            return sum(message.tokens for message in self.messages)

        total_tokens = calc_tokens()
        while (total_tokens > self.max_tokens):
            removed = self.messages.pop(0)
            total_tokens -= removed.tokens
