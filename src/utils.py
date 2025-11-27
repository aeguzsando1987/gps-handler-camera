import datetime
import serial.tools.list_ports
from geopy.distance import geodesic

def listar_puertos_serial():
    """
    Lista todos los puertos serial disponibles en el sistema.
    Retorna: Lista de objetos ListPortInfo
    """
    puertos = serial.tools.list_ports.comports() # Obtenemos todos los puertos serial disponibles usando la libreria serial.tools.list_ports
    return puertos # Retornamos la lista de puertos

def calcular_distancia_metros(coord_1, coord_2):
    """ 
    Calcula la distancia geodosica precisa (GPS) en metros. Usamos la libreria geopy que ya cuenta con la formula geodesica implementada.
    Retorna: Distancia geodosica en metros
    """
    if coord_1 is None or coord_2 is None: # Si alguna de las coordenadas es None, retornamos 0.0
        return 0.0
    return geodesic(coord_1, coord_2).meters # Retornamos la distancia en metros

def generar_timestamp():
    """
    Genera el timestamp con formato YYYYMMDD_HHMMSS_mmm
    Retorna: Timestamp
    """
    # Generar timestamp con formato YYYYMMDD_HHMMSS_mmm. Con [:-3] se quitan los ultimos 3 caracteres y solo dejamos milisegundos
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    

    