from plyer import gps


class Gps:
    def __init__(self):
        try:
            print("comenzando el Gps")
            self.alerta = [[-33.500163752818224, -70.61100120164757]]
            self.datos_relativos = []
            self.comienza_gps()
            print("Gps listo")
        except:
            print('Fallo al activar el gps, revise su conexion o plataforma')
        
    def datos_gps(self, **kwargs):
        datos = f'{lat}, {lon}, {alt}, {spd}'.format(**kwargs)
        cadena = str(datos)
        cadenagps = cadena.split(',')
        lat = cadenagps[0]
        lon = cadenagps[1]
        alt = cadenagps[2]
        spd = cadenagps[3]

        print (f"latitud: {lat} \n longitud: {lon} \n altitude: {alt} \n speed: {spd} \r\n")
        self.datos_relativos = [lat,lon,alt,spd]
        self.bufergps()

    def bufer_gps(self):
        return self.datos_relativos

    def comienza_gps(self, *args):
        if platform == "android":
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                # CALLBACK PARA PERMISOS, REVISA PERMISOS OTORGADOS
                if all([res for res in results]):
                    print('Permisos otorgados')
                    gps.configure(on_location=self.datos_gps)
                    gps.start(minTime = 1000, minDistance = 1)
                else:
                    print("Permisos no otorgados")
        else:
            print("El dispositivo no tiene soporte GPS")
        request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], 
                                    callback)
        
    #def __del__(self):
        #print('hola soy el destructor de la clase gps')