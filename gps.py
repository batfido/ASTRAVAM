from cgitb import text
from kivy.app import App    
from kivy.uix.label import Label
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
from plyer import gps
from kivymd.uix.button import MDRectangleFlatButton

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
            if platform == "android":
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
                app.gps_label.text ="El dispositivo no tiene soporte GPS"
            
        else:
            pass

class WinCheeser():
    def __init__(self, *args, **kwargs):
        return self

    def set_location(*args, **kwargs):
        app = App.get_running_app()
        app.location["lat"]=float(input("Lat"))
        app.lat_label.text=str(app.location["lat"])
        app.location["lon"]=float(input("Lon"))
        app.lon_label.text=str(app.location["lon"])



class GPSOperator():
    def __init__(self) -> None:
        pass
    def start_gps(self, *args, **kwargs):
        perm_manager=PermManager()
        app = App.get_running_app()
        win_cheeser = WinCheeser
        try:
            gps.configure(on_location=self.update_loc, on_status=perm_manager.resolve_permissions)
            gps.start(minTime=100)
        except NotImplementedError or ModuleNotFoundError:
            diag=MDDialog(title="GPS no implementado", text="No se detecta un GPS utilizable por el sistema")
            diag.open()
            app.gps_label.pos_hint={"center_x": 1.08, "center_y": 0.15}
            app.gps_label.text= "No se detecta un GPS utilizable por el sistema"
            win_cheeser.set_location()
            app.cheese_btn=MDRectangleFlatButton(text="Revisa alertas", pos_hint={"center_x": 0.5, "center_y": 0.3})
            app.screen.add_widget(app.cheese_btn)
            app.cheese_btn.bind(on_press = self.check_gps)



    def check_gps():
        app = App.get_running_app()

        pass



    def update_loc(self, *args, **kwargs):
        app = App.get_running_app()
        my_lat=kwargs["lat"]
        my_lon=kwargs["lon"]
        app.gps_label.text =f"Ubicación: Lat:{my_lat} Lon:{my_lon}"
        app.location["lat"]=my_lat
        app.location["lon"]=my_lon
