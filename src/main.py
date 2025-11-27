import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import pandas as pd
import time
from src import utils, config, CLI
from src.gps_reader import GPSHandler
from src.cam_controller import CameraHandler

class PotatoeApp:
    def __init__(self, root, user_config):
        self.root = root
        self.config = user_config
        self.root.title(f"Monitor Visual | mts: {self.config['distance']}")

        if not os.path.exists(config.RGB_DIR): os.makedirs(config.RGB_DIR)
        if not os.path.exists(config.DEPTH_DIR): os.makedirs(config.DEPTH_DIR)

        self.gps = GPSHandler(self.config['gps_port'], self.config['gps_baud'])
        self.gps.start()

        self.camera = CameraHandler()
        self.camera.start()

        self.lastCoords = None
        self.photoId = 1
        self.logdata = []

        self.setupUI()
        self.updateLoop()

    def setupUI(self):
        self.lbl_video = tk.Label(self.root)
        self.lbl_video.grid(row=0, column=0, rowspan=5, padx=10, pady=10)
        font_style = ('Arial', 12)
        self.txt_lat = tk.Label(self.root, text="Lat: ...", font=font_style)
        self.txt_lat.grid(row=0, column=1)
        self.txt_dist = tk.Label(self.root, text="Distancia: 0.0m", font=font_style)
        self.txt_dist.grid(row=1, column=1)
        self.txt_status = tk.Label(self.root, text="Estado: Esperando movimiento... ", font=font_style)
        self.txt_status.grid(row=2, column=1)
        tk.Button(self.root, text="TERMINAR Y GUARDAR", font=font_style, command=self.closeApp).grid(row=4, column=1, sticky="ew")

    def updateLoop(self):
        """
        funcion que se ejecuta 30 veces por segundo para actualizar los datos de la GUI
        """
        color, depth = self.camera.getFrames()
        if color is not None:
            self.processPhotoShoot(color, depth)
            im_rgb = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(im_rgb)
            im_tk = ImageTk.PhotoImage(image=im_pil)
            self.lbl_video.imgtk = im_tk
            self.lbl_video.configure(image=im_tk)

        self.txt_lat.config(text=f"Lat: {self.gps.lat:.6f}, Lon: {self.gps.lon:.6f}")
        self.root.after(30, self.updateLoop)


        
    def processPhotoShoot(self, color, depth):
        if not self.gps.connected or self.gps.speedKmh < config.VELOCIDAD_MINIMA_KMH:
            return
        
        actualPos = (self.gps.lat, self.gps.lon)

        if self.lastCoords is None:
            self.lastCoords = actualPos
            return

        dist = utils.calcular_distancia_metros(self.lastCoords, actualPos)
        self.txt_dist.config(text=f"Acumulado: {dist:.2f}m")

        if dist >= self.config['distance']:
            timestamp = utils.generar_timestamp()
            rgb_path, depth_path = self.camera.saveFrames(color, depth, self.photoId, timestamp)

            fila = {
                "ID": self.photoId,
                "Time": timestamp,
                "Lat": self.gps.lat,
                "Lon": self.gps.lon,
                "Speed": self.gps.speedKmh,
                "Heading": self.gps.heading,
                "RGB_path": rgb_path,
                "Depth_path": depth_path
            }

            self.logdata.append(fila)

            print(f"Fotografia {self.photoId} tomada a {dist:.2f}m | {timestamp}")
            self.txt_status.config(text=f"Ultima foto tomada: {self.photoId} ({timestamp})")

            self.lastCoords = actualPos
            self.photoId += 1

    def closeApp(self):
        print(f"Guardando datos en CSV...")
        if self.logdata:
            df = pd.DataFrame(self.logdata)
            path = os.path.join(config.BASE_DIR, f"log_{utils.generar_timestamp()}.csv")
            df.to_csv(path, index=False)
            print(f"Archivo guardado en {path}")

        self.gps.stop()
        self.camera.stop()
        self.root.destroy()

if __name__ == "__main__":
    conf = CLI.execSetup()
    window = tk.Tk()
    app = PotatoeApp(window, conf)
    window.mainloop()
            


        
       

        
        
        

        

    

    