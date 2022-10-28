from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from plyer import gps
from gps import Gps

class Ui(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        Builder.load_file('design.kv')
        return Ui()
    pass
    def change_switch(self, checked, value):
        if value:
            Gps()
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_palette = 'Red'
        else:
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_palette = 'Teal'
            pass
        
if __name__ == '__main__':
    MainApp().run()

