# peru
import imp
from operator import pos
from turtle import bgcolor, color
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.utils import platform
from plyer import gps
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from gps import GPSConf



class Main(MDApp):
    def build(self):
        screen = MDScreen()
        astralabel = MDLabel(text=f"ASTRAVAM 7w7\nEstas en {platform}", pos={0.5, 0.2})
        screen.add_widget(astralabel)
        start_btn=MDRectangleFlatButton(text="Comienza!", pos_hint={"center_x": 0.5, "center_y": 0.5})
        screen.add_widget(start_btn)
        start_btn.bind(on_press = GPSConf.run)
        return screen
Main().run()