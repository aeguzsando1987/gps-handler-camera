import os
# --- CONFIGURACIONES DE GEOMETRIA DE COSECHAS --- #

DISTANCIA_OBJETIVO_M = 2.0 # n metros que se deben recorrer para que se tome la foto y se realice el registro
VELOCIDAD_MINIMA_KMH = 0.5 # Filtro anti deriva: Como no tenemos RTK, si el gps va muy lento que (mas que esta velocidad), ignora los datos para que evite tomar fotos parado


# --- CONFIGURACIONES DE LA COMPUTADORA (HARDWARE) --- #
# Puertos seriales (en windows 'COM3', Linux '/dev/ttyUSB0')
GPS_PORT = 'COM3'
BASE_DIR = os.path.join(os.getcwd(), 'datos_cosecha') # Log de datos de cosecha con georeferenciacion
RGB_DIR = os.path.join(BASE_DIR, 'rgb') # Directorio de guardado de imagenes RGB
DEPTH_DIR = os.path.join(BASE_DIR, 'depth') # Directorio de guardado de mapas de profundidad


