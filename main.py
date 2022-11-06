from kivy.app import App
from kivymd.app import MDApp
from kivy.utils import platform
from plyer import gps
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.core.audio import SoundLoader
from kivymd.uix.dialog import MDDialog
from time import time
from os import path

class Main(MDApp):
    def build(self):
        self.alerta={"lat": -33.50014982162118, "lon": -70.61100904550202} # -33.50014982162118, -70.61100904550202
        self.gps_stat=False
        self.location={"lat": "NA", "lon": "NA"}
        self.screen = MDScreen()
        self.gps_label=MDLabel(text="No hay informacion del GPS", pos_hint={"center_x": 1.2, "center_y": 0.15})
        self.screen.add_widget(self.gps_label)
        self.start_btn=MDRectangleFlatButton(text="Comienza!", pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.screen.add_widget(self.start_btn)
        self.start_btn.bind(on_press = self.call_gps)
        self.lat_label=MDLabel(text=self.location["lat"], pos_hint={"center_x": 1.2, "center_y": 0.1})
        self.screen.add_widget(self.lat_label)
        self.lon_label=MDLabel(text=self.location["lon"], pos_hint={"center_x": 1.2, "center_y": 0.05})
        self.screen.add_widget(self.lon_label)
        return self.screen
    def call_gps(self,*args):
        gpsd.run()

class GPSOperator():
    def __init__(self) -> None:
        self.id = "op"
        self.last_played=-99999999999999999999999
    def run(*args):

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    from plyer import gps
                    gps.configure(on_location=self.update_blinker_position,
                                  on_status=self.on_auth_status)
                    gps.start(minTime=1000, minDistance=0)
                else:
                    print("Did not get all permissions")

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)

        # Configure GPS
        if platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.check_gps,
                          on_status=self.on_auth_status)
            gps.start(minTime=1000, minDistance=0)


    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()

    def check_gps(*args, **kwargs):
        self = args[0]
        app = App.get_running_app()
        lat = app.location["lat"]
        lon = app.location["lon"]
        a_lat = app.alerta["lat"]
        a_lon = app.alerta["lon"]
        if a_lat - 0.0001 < lat < a_lat + 0.0001 and a_lon - 0.0001 < lon < a_lon + 0.0001:
            print(a_lat - 0.0001 < lat < a_lat + 0.0001 and a_lon - 0.0001 < lon < a_lon + 0.0001)
            self.alertar_pare(time())
        self.update_loc()

    
    def alertar_pare(*args, **kwargs):
        alerta = SoundLoader.load(path.join("resources","Pare_50m.mp3"))
        print(alerta)
        if time()-args[0].last_played >=3:
            alerta.seek(0)
            args[0].last_played=time()
            alerta.play()
            print("reproduciendo alerta")

        app.location["lon"]=my_lon

    def update_loc(self, *args, **kwargs):
        app = App.get_running_app()
        my_lat=kwargs["lat"]
        my_lon=kwargs["lon"]
        app.gps_label.text =f"Ubicación: Lat:{my_lat} Lon:{my_lon}"
        app.location["lat"]=my_lat
        app.location["lon"]=my_lon
gpsd = GPSOperator()
Main().run()