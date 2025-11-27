import pyrealsense2 as rs
import numpy as np
import cv2
import os
from src import config

class CameraHandler:
    def __init__(self):
        self.pipeline = rs.pipeline() # Pipeline para datos de la camara.
        self.config = rs.config()
        # Resolucion de la camara a 640x480 con 30 fps. Configurar segun la camara (640x480, 1280x720, 1920x1080). Preguntar a JP
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        # Resolucion para el stream de profundidad a 640x480 con 30 fps. 
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    def start(self):
        """
        Inicia la camara y espera a que se estabilice.
        Retorna: True si la camara se inicia correctamente, False en caso contrario
        """
        try:
            self.pipeline.start(self.config)
            for _ in range(10):
                # Por defecto hacemos que se descarten los primeros 10 frames para que la camara se estabilice segun condiciones de luz.
                self.pipeline.wait_for_frames()
                print("Camara lista para captura")
                return True
        except Exception as e:
            print(f"Error al iniciar la camara: {e}")
            return False

    def getFrames(self):
        """
        Obtiene las imagenes y la profundidad de la camara
        Retorna: frames de la camara
        """
        try:   
            # Bloqueamos la camara para obtener los frames sincronicamente
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            # Si no se obtienen los frames, retornar None
            if not color_frame or not depth_frame:
                return None, None
            
            # Convertimos los frames a matrices
            color_frame = np.asanyarray(color_frame.get_data())
            depth_frame = np.asanyarray(depth_frame.get_data())
            
            return color_frame, depth_frame
        except Exception as e:
            print(f"Error al obtener frames: {e}")
            return None, None

    def saveFrames(self, color_frame, depth_frame, index, timestamp):
        """
        Guarda los frames de la camara en archivos
        Retorna: path de los archivos guardados
        """
        filename = f"{index}_{timestamp}"
        
        path_rgb = os.path.join(config.RGB_DIR, filename + '_rgb.png')
        cv2.imwrite(path_rgb, color_frame)

        path_depth = os.path.join(config.DEPTH_DIR, filename + '_depth.npy')
        np.save(path_depth, depth_frame)

        return path_rgb, path_depth

    def stop(self):
        """
        Detiene la camara
        """
        self.pipeline.stop()

    