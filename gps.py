from cgitb import text
from kivy.app import App    
from kivy.uix.label import Label
from kivy.utils import platform
from plyer import gps
from kivymd.uix.dialog import MDDialog

class GPSConf():
    def run(*args,**kwargs):
        # Permisos: ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION
        print("boton apretado")
        dialog = MDDialog(title="Equisde", text= "Aun no hay codigo para esto")
        dialog.open()
        pass
        
