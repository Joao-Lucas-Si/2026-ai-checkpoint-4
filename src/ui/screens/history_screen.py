import os

from prompt_toolkit import PromptSession
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt

from src.schemas import AnaliseSchema
from src.chain import main_pipeline, pipeline
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

def userMessage(message: dict, console: Console):
    width = int(console.width/2.5)
    panel = Panel(Markdown(message["content"], justify="right",), width=width,padding=(1, 2),  border_style="#93358D")
    return Align.right(Padding(panel,pad=(0,2)), )

def chatMessage(message: dict, console: Console):
    width = int(console.width/2.5)
    panel = Panel(Markdown(message["content"]), padding=(1, 2),  title="chatbot", width=width, expand=True, title_align="left", border_style="#FFB71B")
    return Align.left(Padding(panel, pad=(0,2)))

class HistoruScreen(Screen):
    messages = [
      
    ]
    
    def drawMessage(self, console: Console):
        clean()
        layout = Layout()
            
        layout.split_row(
            Layout(name="chat"),
            Layout(name="user"),
        )
        width = int(console.width/2.5)
        for message in self.messages:
            if message["type"] == "user":
                
                
                console.print(userMessage(message, console))
            else:
                
                console.print(chatMessage(message, console))
         
        # console.log(layout)           
    
    def draw(self, console: Console):
     
        while True:
            
            self.drawMessage(console)
   
            prompt = Session.get_session("mensagens").prompt("sua mensagem: ", )
            
            self.messages.append({
                "type": "user",
                "content": prompt
            })

            self.drawMessage(console)
           
            response = main_pipeline(prompt)

            self.messages.append({
                "type": "chat",
                "content": response
            })