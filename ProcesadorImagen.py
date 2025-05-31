import matplotlib.pyplot as plt
import numpy as np
import cv2

class ProcesadorImagen:
    def __init__(self, ruta=None):
        self.imagen_original = None
        if ruta:
            self.cargar_imagen(ruta)
        self.imagen_grises = None
        self.imagen_umbral = None
        self.ecualizada_hipercubica = None
        self.imagen_suma = None
        self.imagen_resta = None
        self.imagen_multiplicacion = None
    
    def cargar_imagen(self, ruta):
        self.imagen_original = cv2.imread(ruta)
        if self.imagen_original is not None:
            self.imagen_original = cv2.resize(self.imagen_original, (400, 400))
        return self.imagen_original

    def convertir_a_grises(self, img):
        if img is None:
            return None
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def aplicar_binarizacion(self, img, umbral):
        

        _, self.imagen_umbral = cv2.threshold(img, umbral, 255, cv2.THRESH_BINARY)
        return self.imagen_umbral

    def calcular_histogramas(self):
        if self.imagen_grises is None:
            self.convertir_a_grises()
        if self.imagen_grises is None:
            return None, None

        # Histograma en escala de grises
        fig_gray = plt.figure(figsize=(4, 3))
        plt.hist(self.imagen_grises.ravel(), 256, [0, 256])
        plt.title('Histograma en Escala de Grises')

        # Histograma por canales de color
        fig_color = plt.figure(figsize=(4, 3))
        colores = ('b', 'g', 'r')
        for i, canal in enumerate(colores):
            histograma = cv2.calcHist([self.imagen_original], [i], None, [256], [0, 256])
            plt.plot(histograma, color=canal)
        plt.title('Histograma de la Imagen en Color')
        plt.xlim([0, 256])
        
        return fig_gray, fig_color

    def ecualizacion_hipercubica(self, img):
        
        g_min = np.min(img)
        g_max = np.max(img)

        histograma, _ = np.histogram(img, bins=256, range=(0, 255))
        probabilidades = histograma / np.sum(histograma)
        suma_acumulada = np.cumsum(probabilidades)

        cubo_min = np.cbrt(g_min)
        cubo_max = np.cbrt(g_max)

        tabla_transformacion = np.array([
            ((cubo_max - cubo_min) * suma_acumulada[g] + cubo_min) ** 3 for g in range(256)
        ])
        tabla_transformacion = np.clip(tabla_transformacion, 0, 255).astype(np.uint8)
        ecualizada_hipercubica = tabla_transformacion[img]
        return ecualizada_hipercubica
