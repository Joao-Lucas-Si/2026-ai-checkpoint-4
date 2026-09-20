from abc import ABC


class Process[Context](ABC):
    context: Context
    
    def execute(self):
        ...