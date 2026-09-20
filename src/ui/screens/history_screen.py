import os

from prompt_toolkit import PromptSession
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt

from src.chain import pipeline
from src.ui.elements.screen import Screen

input = Prompt

class Session():
    
    
    
    sessions: dict[str, PromptSession] = {}
    
    @staticmethod
    def get_session(name: str):
        if name in Session.sessions:
            return Session.sessions[name]
        
        session = PromptSession()
        Session.sessions[name] = session
        return session
    
def clean():
    os.system('cls' if os.name == 'nt' else 'clear')

class HistoruScreen(Screen):
    messages = [
        {"type": "user", "content": "*oi*", "time": "14:00"},
        {"type": "chat", "content": "oi, como posso ajudar", "time": "14:01"},
    ]
    
    def drawMessage(self, console: Console):
        # clean()
        layout = Layout()
            
        layout.split_row(
            Layout(name="chat"),
            Layout(name="user"),
        )
        width = int(console.width/2.5)
        for message in self.messages:
            if message["type"] == "user":
                panel = Panel(Markdown(message["content"], justify="right",), width=width,padding=(1, 2),  border_style="#93358D")
                
                console.print(Align.right(Padding(panel,pad=(0,2)), ))
            else:
                panel = Panel(Markdown(message["content"]), padding=(1, 2),  title="chatbot", width=width, expand=True, title_align="left", border_style="#FFB71B")
                console.print(Align.left(Padding(panel, pad=(0,2))))
         
        # console.log(layout)           
    
    def draw(self, console: Console):
     
        while True:
            
            self.drawMessage(console)
            choice = input.ask("ação", choices=["perguntar", "resumo", "expansao", "brainstorm"], console=console)

            prompt = Session.get_session(choice).prompt("sua mensagem: ", )
            
            self.messages.append({
                "type": "user",
                "content": prompt
            })
            self.drawMessage(console)
            response = pipeline(choice, prompt)
            
            self.messages.append({
                "type": "chat",
                "content": response
            })