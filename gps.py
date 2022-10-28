from plyer import gps
import time

class Gps:
    def __init__(self):
        try:
            print("comenzando el Gps")
            self.disco_pare = [-33.500195465448776, -70.61154519632926]
            self.alerta = [-33.500163752818224, -70.61100120164757]
            self.datos_relativos = ''
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
        self.datos_relativos = "\t"+lat+"\t"+lon+"\t"+alt+"\t"+spd+"\t\r\n"
        self.bufergps()

    def bufer_gps(self):
        self.comparar_ubicacion(self.datos_relativos)
        return self.datos_relativos
    def comienza_gps(self, *args):
        try:
            gps.configure(on_location=self.datos_gps)
            if True:
                gps.start()
                self.datos_relativos=self.bufer_gps()
        except:
            self.datos_relativos = 0
            print(self.datos_relativos)
            pass
        return self.datos_relativos

    def comparar_ubicacion(self, datos):
        if datos[0] == str(self.alerta[0]) and datos[1] == str(self.alerta[1]):
            print('hay un disco pare a 50 metros')
        else:
            print('no hay disco pare cercano')

    def __del__(self):
        print('hola soy el destructor de la clase gps')