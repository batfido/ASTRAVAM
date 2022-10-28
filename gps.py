from cgitb import text
from kivy.app import App    
from kivy.uix.label import Label
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog

class GPSConf():
    def __init__(self):
        self.id="xd"
        pass
    def run(*args):
        print(args)
        # Permisos: ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION
        print("boton apretado")
        gps_op=GPSOperator()
        #if platform=="android":
        #    gps_op.start_gps()
        gps_op.start_gps()
        # gps.configure(on_location=perm_manager.update_loc, on_status=gps_op.resolve_permissions)

class PermManager():
    def __init__(self) -> None:
        pass

    def resolve_permissions(self, *args, **kwargs):
        if not App.get_running_app().gps_stat:
            app = App.get_running_app()
        #   if platform == "android":
            if platform != "android":
                app.gps_label.text ="El dispositivo no tiene soporte GPS"
            else:
                from android.permissions import Permission, request_permissions
                def callback(permission, results):
                    # CALLBACK PARA PERMISOS, REVISA PERMISOS OTORGADOS
                    if all([res for res in results]):
                        print('Permisos otorgados')
                    else:
                        print("Permisos no otorgados")
                request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], 
                                    callback)
        else:
            pass




class GPSOperator():
    def __init__(self) -> None:
        pass
    def start_gps(self, *args, **kwargs):
        from plyer import gps
        perm_manager=PermManager()
        try:
            gps.configure(on_location=self.update_loc, on_status=perm_manager.resolve_permissions)
            gps.start(minTime=100)
        except NotImplementedError or ModuleNotFoundError:
            diag=MDDialog(title="GPS no implementado", text="No se detecta un GPS utilizable por el sistema")
            diag.open()

    def update_loc(self, *args, **kwargs):
        app = App.get_running_app()
        my_lat=kwargs["lat"]
        my_lon=kwargs["lon"]
        app.gps_label.text =f"Ubicación: Lat:{my_lat} Lon:{my_lon}"
        app.location["lat"]=my_lat
        app.location["lon"]=my_lon
        