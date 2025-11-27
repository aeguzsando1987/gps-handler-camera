# Sistema de Monitoreo de Cosecha Georeferenciado

Sistema de monitoreo de precision agricola que captura imagenes georeferenciadas durante operaciones de cosecha, utilizando GPS y camaras de profundidad Intel RealSense.

## Descripcion

Este proyecto integra sensores GPS con camaras de vision por computadora para crear un sistema de monitoreo de cosecha. El sistema registra automaticamente imagenes RGB y mapas de profundidad cuando se alcanza una distancia objetivo especificada, permitiendo analisis detallado de cultivos con informacion geoespacial precisa.

### Caracteristicas Principales

- Captura de imagenes automatica basada en distancia GPS recorrida
- Integracion de camara Intel RealSense para imagenes RGB y profundidad
- Filtro anti-deriva para evitar capturas cuando el equipo esta estatico
- Calculos geodesicos precisos usando la libreria geopy
- Sistema de hilos (threading) para lectura GPS sin bloqueo
- Timestamps con precision de milisegundos para correlacion de datos

## Requisitos del Sistema

(por definir)

### Hardware

- Receptor GPS con salida NMEA (puerto serial)
- Camara Intel RealSense (compatible con pyrealsense2)
- Puerto serial disponible (COM3 en Windows, /dev/ttyUSB0 en Linux)

### Software

- Python 3.x
- OS: Windows, Linux o Mac
- Dependencias listadas en requirements.txt

## Instalacion

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd code
```

2. Crear y activar entorno virtual:

En Windows:
```bash
python -m venv env
env\Scripts\activate
```

En Linux/Mac:
```bash
python -m venv env
source env/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuracion

Editar el archivo `src/config.py` para ajustar los parametros del sistema:

### Parametros de Geometria de Cosecha

- `DISTANCIA_OBJETIVO_M`: Distancia en metros entre capturas (por defecto: 2.0 metros)
- `VELOCIDAD_MINIMA_KMH`: Velocidad minima en km/h para filtrar deriva GPS (por defecto: 0.5 km/h)

### Configuracion de Hardware

- `GPS_PORT`: Puerto serial del GPS
  - Windows: 'COM3', 'COM4', etc.
  - Linux: '/dev/ttyUSB0', '/dev/ttyACM0', etc.

## Estructura del Proyecto

```
code/
|-- src/
|   |-- config.py         # Parametros de configuracion del sistema
|   |-- gps_reader.py     # Clase GPSHandler para lectura GPS
|   |-- utils.py          # Funciones utilitarias
|   |-- __init__.py
|
|-- datos_cosecha/        # Directorio de salida de datos
|   |-- rgb/              # Imagenes RGB capturadas
|   |-- depth/            # Mapas de profundidad capturados
|
|-- env/                  # Entorno virtual de Python
|-- requirements.txt      # Dependencias del proyecto
|-- README.md             # Este archivo
|-- CLAUDE.md             # Guia para Claude Code
```

## Modulos Principales

### src/config.py

Archivo de configuracion central que contiene todos los parametros ajustables del sistema:
- Distancia objetivo entre capturas
- Velocidad minima para filtro anti-deriva
- Puerto serial del GPS

### src/gps_reader.py

Implementa la clase `GPSHandler` que maneja la comunicacion serial con el GPS:
- Lectura en hilo secundario (daemon thread) para no bloquear la aplicacion
- Parsing de tramas NMEA para extraer latitud, longitud, velocidad y rumbo
- Conversion de formato NMEA a coordenadas decimales
- Propiedades compartidas thread-safe para integracion con GUI

### src/utils.py

Funciones utilitarias del sistema:
- `listar_puertos_serial()`: Enumera puertos seriales disponibles
- `calcular_distancia_metros()`: Calcula distancia geodesica entre coordenadas GPS
- `generar_timestamp()`: Genera timestamps en formato YYYYMMDD_HHMMSS_mmm

## Uso

1. Conectar el receptor GPS al puerto serial configurado
2. Conectar la camara Intel RealSense
3. Verificar la configuracion en `src/config.py`
4. Ejecutar el script principal (pendiente de implementacion)

El sistema comenzara a capturar imagenes automaticamente cada vez que se recorra la distancia objetivo configurada, siempre que la velocidad sea mayor al umbral minimo.

## Datos de Salida

Los datos capturados se almacenan en el directorio `datos_cosecha/`:
- `rgb/`: Imagenes a color capturadas por la camara
- `depth/`: Mapas de profundidad correspondientes

Los archivos se nombran con timestamps precisos para permitir correlacion con datos GPS.

## Filtro Anti-Deriva

El sistema implementa un filtro de velocidad minima para evitar capturas erroneas cuando el equipo esta estatico. Si la velocidad GPS es menor a `VELOCIDAD_MINIMA_KMH`, el sistema ignora los datos para prevenir registros por deriva GPS.

## Calculos Geodesicos

El sistema utiliza la libreria `geopy` para calculos de distancia precisos que toman en cuenta la curvatura de la Tierra, esencial para precision en agricultura de precision.

## Status del Proyecto

En desarrollo

## Licencia

MIT License. Uso libre para fines educativos y de investigación.

## Autores

Autor principal: E. Guzman

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crear un issue o pull request para sugerencias y mejoras.
