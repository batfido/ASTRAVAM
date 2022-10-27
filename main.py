# peru
from kivy.app import App    
from kivy.uix.label import Label
from kivy.utils import platform



class Main(App):
    def build(self):
        return Label(text=f"ASTRAVAM 7w7\nEstas en {platform}")

Main().run()