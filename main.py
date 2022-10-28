from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

from plyer import gps
from gps import Gps

class Ui(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')
        root = MDScreen()
        return Ui()
    pass

    def play_alerta(*args):
        sound = SoundLoader.load('sonido_alerta.mp3')
        sound.play()
    def change_switch(self, checked, value):
        if value:
            señal_gps = Gps()
            for disco_pare in señal_gps.alerta:
                if disco_pare[0] == str(señal_gps.alerta[0]) and disco_pare[1] == str(señal_gps.alerta[1]):
                    print('hay un disco pare a 40 metros')
                    self.play_alerta()
                else:
                    print('no hay un disco pare cercano, o la zona no tiene suficiente informacion')
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_palette = 'Red'
        else:
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_palette = 'Teal'
        
if __name__ == '__main__':
    MainApp().run()

