import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import stats 

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
    
    def filtro_mediana(self):
        print("aplicando filtro mediana")
        if self.imagen_original is None:
            return None
        imagen_mediana = cv2.medianBlur(self.imagen_original,5)
        return imagen_mediana
    
    def filtro_moda(self, kernel_size=3):
        print("aplicando filtro Moda")

        if self.imagen_original is None:
            return None 
        imagen = self.imagen_original
        salida = np.copy(imagen)
        h, w, c = imagen.shape
        pad = kernel_size // 2

        # Rellenar por canal
        imagen_padded = np.pad(imagen, ((pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0)

        for i in range(h):
            for j in range(w):
                for ch in range(c):  # Aplicar por canal
                    window = imagen_padded[i:i + kernel_size, j:j + kernel_size, ch]
                    moda = stats.mode(window, axis=None, keepdims=False).mode
                    salida[i, j, ch] = moda

        return salida
    
    