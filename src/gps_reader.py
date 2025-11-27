import threading
import serial
import threading
import time

class GPSHandler:
    def __init__(self, port, baud=9600):
        # Guardar configuracion que ingresa usuario al inicio
        self.port = port
        self.baud = baud

        # Datos que se comparten y se visualizan en GUI
        self.connected = False
        self.lat = 0.0
        self.lon = 0.0
        self.speedKmh = 0.0 # Velocidad en km/h importante para filtrar fotos al estar estatico
        self.heading = 0.0 # Rumbo. Se espera que salga de trama GPRMC

        self.running = False # Indicar encendido o apagado del thread

    def start(self):
        """
        Inicia el thread secundario para la lectura del GPS
        """
        self.running = True
        # Iniciar thread secundario. daemon=True para que mate el thread cuando se cierre el programa
        t = threading.Thread(target=self._worker, daemon=True) 
        t.start()

    def _worker(self):
        """
        Funcion que se ejecuta en el thread secundario en paralelo al loop principal
        """
        try:
            # Iniciar la comunicacion serial. timeout=1 para que no se quede bloqueado si no hay respuesta
            ser = serial.Serial(self.port, self.baud, timeout=1)
            self.connected = True
            print(f"GPS conectado a {self.port} a {self.baud} baudios")
        except Exception as e:
            print(f"Error al conectar al GPS: {e}")
            self.connected = False
            return
        
    def NMEAtoDecimal(self, value, direction):
        """
        Convierte los valores de las tramas NMEA a decimal
        """
        if not value: return 0.0 # Si el valor es None, retornamos 0.0
        deg = int(float(value) / 100) # Obtenemos los grados
        minutes = float(value) - (deg * 100) # Obtenemos los minutos. Necesario para convertir a decimal
        res = deg + (minutes / 60) # Convertimos a decimal
        return -res if direction in ['S', 'W'] else res # Si es sur o oeste, retornamos negativo

    def stop(self):
        """
        Detiene el thread secundario
        """
        self.running = False
        
   

