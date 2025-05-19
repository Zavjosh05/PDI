import numpy as np
import cv2
import matplotlib.pyplot as plt

#En esta claser iran los filtros de pasa altas y pasa bajas
class Filtros:
    def __init__(self, imagen=None):
        self.imagen_original = imagen

    def filtro_promediador(self):
        print("aplicando filtro promediador")
        if self.imagen_original is None:
            print("Error en la lectura de imagen filtro promediador")
            return None
        else: 
            print("lectura de imagen exitosa imagen filtro promediador")
        imagen_filtrada = cv2.blur(self.imagen_original, (5,5))
        return imagen_filtrada      
    
    def filtro_pesado(self):
        if self.imagen_original is None:
            return None
        kernel = np.array([[1, 1, 1], [1, 5, 1], [1, 1, 1]]) / 13
        imagen_promediador_pesado = cv2.filter2D(self.imagen_original, -1, kernel)
        return imagen_promediador_pesado
    
    def filtro_gaussiano(self):
        print("aplicando filtro gaussiano")
        if self.imagen_original is None:
            return None
        imagen_gaussiana = cv2.GaussianBlur(self.imagen_original, (5,5), 1)
        return imagen_gaussiana
    
    
    