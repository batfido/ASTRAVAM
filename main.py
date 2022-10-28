# peru
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

gpsd=GPSConf

class Main(MDApp):
    def build(self):
        self.gps_stat=False
        self.location=dict()
        self.screen = MDScreen()
        self.gps_label=MDLabel(text="No hay informacion del GPS", pos_hint={"center_x": 1.2, "center_y": 0.05})
        self.screen.add_widget(self.gps_label)
        self.start_btn=MDRectangleFlatButton(text="Comienza!", pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.screen.add_widget(self.start_btn)
        self.start_btn.bind(on_press = self.call_gps)
        return self.screen
    def call_gps(self,*args):
        gpsd.run()
Main().run()