import threading
import serial
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

        # Loop principal de lectura continua de datos GPS
        while self.running:
            try:
                # Leer linea del puerto serial
                line = ser.readline().decode('ascii', errors='ignore').strip()

                # Verificar si es una trama NMEA valida
                if not line.startswith('$'):
                    continue

                # Separar los campos de la trama NMEA
                parts = line.split(',')

                # Procesar trama GPRMC (para latitud y longitud)
                # Formato: $GPRMC,time,status,lat,N/S,lon,E/W,speed,heading,date,...
                if parts[0] == '$GPRMC' and len(parts) >= 7:
                    # Verificar que la trama sea valida (status = 'A' = Active)
                    if parts[2] == 'A':
                        # Extraer latitud y longitud
                        self.lat = self.NMEAtoDecimal(parts[3], parts[4])
                        self.lon = self.NMEAtoDecimal(parts[5], parts[6])

                # Procesar trama GPVTG (para velocidad en km/h y heading)
                # Formato: $GPVTG,heading,T,heading,M,speed_knots,N,speed_kmh,K,mode*checksum
                elif parts[0] == '$GPVTG' and len(parts) >= 8:
                    # Extraer heading (rumbo)
                    try:
                        self.heading = float(parts[1]) if parts[1] else 0.0
                    except:
                        self.heading = 0.0

                    # Extraer velocidad en km/h (campo 7, marcado con 'K')
                    try:
                        self.speedKmh = float(parts[7]) if parts[7] else 0.0
                    except:
                        self.speedKmh = 0.0

            except Exception as e:
                print(f"Error al leer GPS: {e}")
                time.sleep(0.1)

        # Cerrar conexion serial al terminar
        ser.close()
        self.connected = False
        print("GPS desconectado")
        
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
        
   

