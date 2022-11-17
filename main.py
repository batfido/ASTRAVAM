from kivy.app import App
from kivymd.app import MDApp
from kivy.utils import platform
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.core.audio import SoundLoader
from kivymd.uix.dialog import MDDialog
from time import time
from os import path
'''
Android GPS
-----------
'''

from plyer.facades import GPS
from plyer.platforms.android import activity
from jnius import autoclass, java_method, PythonJavaClass

Looper = autoclass('android.os.Looper')
LocationManager = autoclass('android.location.LocationManager')
Context = autoclass('android.content.Context')


class _LocationListener(PythonJavaClass):
    __javainterfaces__ = ['android/location/LocationListener']

    def __init__(self, root):
        self.root = root
        super().__init__()

    @java_method('(Landroid/location/Location;)V')
    def onLocationChanged(self, location):
        self.root.on_location(
            lat=location.getLatitude(),
            lon=location.getLongitude(),
            speed=location.getSpeed(),
            bearing=location.getBearing(),
            altitude=location.getAltitude(),
            accuracy=location.getAccuracy())

    @java_method('(Ljava/lang/String;)V')
    def onProviderEnabled(self, status):
        if self.root.on_status:
            self.root.on_status('provider-enabled', status)

    @java_method('(Ljava/lang/String;)V')
    def onProviderDisabled(self, status):
        if self.root.on_status:
            self.root.on_status('provider-disabled', status)

    @java_method('(Ljava/lang/String;ILandroid/os/Bundle;)V')
    def onStatusChanged(self, provider, status, extras):
        if self.root.on_status:
            s_status = 'unknown'
            if status == 0x00:
                s_status = 'out-of-service'
            elif status == 0x01:
                s_status = 'temporarily-unavailable'
            elif status == 0x02:
                s_status = 'available'
            self.root.on_status('provider-status', '{}: {}'.format(
                provider, s_status))


class AndroidGPS(GPS):

    def _configure(self):
        if not hasattr(self, '_location_manager'):
            self._location_manager = activity.getSystemService(
                Context.LOCATION_SERVICE
            )
            self._location_listener = _LocationListener(self)

    def _start(self, **kwargs):
        min_time = kwargs.get('minTime')
        min_distance = kwargs.get('minDistance')
        providers = self._location_manager.getProviders(False).toArray()
        for provider in providers:
            self._location_manager.requestLocationUpdates(
                provider,
                min_time,  # minTime, in milliseconds
                min_distance,  # minDistance, in meters
                self._location_listener,
                Looper.getMainLooper())

    def _stop(self):
        self._location_manager.removeUpdates(self._location_listener)

gps=AndroidGPS()

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
        gpsd = GPSOperator()
        gpsd.run()

class GPSOperator():
    def __init__(self) -> None:
        self.id = "op"
        self.last_played=-99999999999999999999999
    def run(*args):

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            print("imported Android permissions")
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    print("configuring gps")
                    gps.configure(on_location=self.update_blinker_position,
                                  on_status=self.on_auth_status)
                    gps.start(minTime=333, minDistance=0)
                else:
                    print("Did not get all permissions")
            print("requesting Android permissions")
            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)

        # Configure GPS
        if platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.check_gps,
                          on_status=self.on_auth_status)
            gps.start(minTime=333, minDistance=0)


    def on_auth_status(self, general_status, status_message):
        print("revisando status de autenticacion")
        if general_status == 'provider-enabled':
            pass
        else:
            print("Autenticacion fallida")
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


    def update_loc(self, *args, **kwargs):
        app = App.get_running_app()
        my_lat=kwargs["lat"]
        my_lon=kwargs["lon"]
        app.gps_label.text =f"Ubicación: Lat:{my_lat} Lon:{my_lon}"
        app.location["lat"]=my_lat
        app.location["lon"]=my_lon
Main().run()
