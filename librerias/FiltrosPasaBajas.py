import cv2
import numpy as np

class FiltrosPasaBajas:

    def __init__(self):
        self.imagen_original = None
# 1. Filtro promediador (box blur)
    def filtro_promediador(self, img):
        kernel_size = 5
        img_promediador = cv2.blur(img, (kernel_size, kernel_size))
        return img_promediador

# 2. Filtro promediador pesado (weighted average)
    def filtro_promediador_pesado(self, img, k=5):
        kernel_pesado = np.array([[1, 2, 1],
                                [2, k, 2],
                                [1, 2, 1]]) / (8+k)
        img_pesado = cv2.filter2D(img, -1, kernel_pesado)
        return img_pesado

# 3. Filtro mediana
    def filtro_mediana(self, img):
        kernel_size = 5
        img_mediana = cv2.medianBlur(img, kernel_size)
        return img_mediana

# 4. Filtro moda (implementación manual)
    def mode_filter(self, img, size=3):
        pad = size//2
        padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REFLECT)
        result = np.zeros_like(img)
        
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                window = padded[i:i+size, j:j+size]
                values, counts = np.unique(window, return_counts=True)
                result[i,j] = values[np.argmax(counts)]
        return result

# 5. Filtro bilateral
    def filtro_bilateral(self, img):
        img_bilateral = cv2.bilateralFilter(img, 9, 75, 75)
        return img_bilateral

# 6. Filtros máximo y mínimo
    def filtro_max(self, img):
        img_maximo = cv2.dilate(img, np.ones((kernel_size,kernel_size)))
        return img_maximo
    
    def filtro_min(self, img):
        img_minimo = cv2.erode(img, np.ones((kernel_size,kernel_size)))
        return img_minimo

# 7. Filtro gaussiano
    def filtro_gaussiano(self, img):
        img_gaussiano = cv2.GaussianBlur(img_rayleigh, (kernel_size, kernel_size), 0)
        return img_gaussiano