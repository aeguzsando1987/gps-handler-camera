import sys
from src import utils

def execSetup():
    """
    Ejecuta el setup del sistema
    """
    print("\nMONITOR VISUAL GPS")
    print("-"*40)

    print("Detectando puertos serial...")
    ports = utils.listar_puertos_serial()
    print(f"Puertos detectados: {len(ports)}")
    if not ports:
        print("No se detectaron puertos serial o usb")
        sys.exit()
    for i, p in enumerate(ports):
        print(f"{i}. {p.device} - {p.description}")

    idx = -1
    while idx < 0 or idx >= len(ports):
        try:
            val = input("Seleccione un puerto valido: ")
            idx = int(val)
        except:
            pass

    selectedPort = ports[idx].device

    distance = 0.0
    while distance <= 0:
        try:
            val = input("Ingrese la distancia objetivo en metros: ")
            distance = float(val)
        except:
            pass

    return {
        "gps_port": selectedPort,
        "gps_baud": 4800, # standar en AG leader
        "distance": distance
    }
    


    