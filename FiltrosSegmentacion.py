import numpy as np
import cv2
import matplotlib.pyplot as plt


#En esta claser iran los filtros de segmentacion y su umbralizado

class FiltrosSegmentacion:
    def __init__(self, imagen=None):
        self.imagen_original = imagen

    def filtro_Robert(self):
        if self.imagen_original is None:
            print("Error en la lectura de imagen Filtro Robert")
            return None
        else: 
            print("lectura de imagen exitosa imagen Filtro Robert")
        #asegurar la conversion a escala de grises

        self.imagen_original = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
         
        # Definir el kernel de Robert
        kernel_roberts_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
        kernel_roberts_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        # Aplicar el filtro
        bordes_roberts_x = cv2.filter2D(self.imagen_original, -1, kernel_roberts_x)
        bordes_roberts_y = cv2.filter2D(self.imagen_original, -1, kernel_roberts_y)
        imagen_bordes_roberts = cv2.addWeighted(bordes_roberts_x, 0.5, bordes_roberts_y, 0.5, 0)

        if(imagen_bordes_roberts.any()): 
            print("obtencion de bordes exitosas")
        return imagen_bordes_roberts
        
    def filtro_otsu(self):
        if self.imagen_original is None:
            print("Error en la lectura de imagen segmentación otsu")
            return None
        else: 
            print("lectura de imagen exitosa imagen segmentación otsu")
        
        #asegurar la conversion a escala de grises
        self.imagen_original = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)

        # Método de Otsu
        _, umbral_otsu = cv2.threshold(self.imagen_original, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Mostrar la imagen segmentada
        '''plt.figure(figsize=(6, 6))
        plt.imshow(umbral_otsu, cmap='gray')
        plt.title('Segmentación - Método de Otsu')
        plt.axis('off')
        plt.show()'''
        if(umbral_otsu.any()): 
            print("obtencion de umbral otsu exitosa")
        return umbral_otsu
