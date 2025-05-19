import numpy as np
import cv2
import matplotlib.pyplot as plt

#En esta claser iran los filtros de pasa altas y pasa bajas
class Filtros:
    def __init__(self, imagen=None):
        self.imagen_original = imagen

    def filtro_pesado(self):
        if self.imagen_original is None:
            return None
        kernel = np.array([[1, 1, 1], [1, 5, 1], [1, 1, 1]]) / 13
        imagen_promediador_pesado = cv2.filter2D(self.imagen_original, -1, kernel)
        return imagen_promediador_pesado
    
    