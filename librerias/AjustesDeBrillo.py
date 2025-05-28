import cv2
import numpy as np

class AjustesDeBrillo:

    def __init__(self):
        self.imagen_original = None
        self.imagen_ecualizada = None
        self.imagen_gamma = None
        self.imagen_expandida = None

    # # 1. Ecualización del histograma estándar
    def ecualizacion_de_histograma(self, img):
        img_eq = cv2.equalizeHist(img)
        hist_eq = cv2.calcHist([img_eq], [0], None, [256], [0, 256])

# # 2. Corrección Gamma 
    def correccion_gamma(self, img):
        gamma = 0.3
        img_gamma = np.power(img/255.0, gamma) * 255
        img_gamma = img_gamma.astype('uint8')
        hist_gamma = cv2.calcHist([img_gamma], [0], None, [256], [0, 256])

# # 3. Expansión lineal de contraste
    def expansion_lineal_de_contraste(self, img):
        min_val = np.min(img)
        max_val = np.max(img)
        img_expanded = ((img - min_val) / (max_val - min_val)) * 255
        img_expanded = img_expanded.astype('uint8')
        hist_expanded = cv2.calcHist([img_expanded], [0], None, [256], [0, 256])

# # 4. Transformación Exponencial
    def transformacion_exponencial(self, img):
        c = 1.0
        exponent = 0.05
        img_exp = c * (1 - np.exp(-img * exponent))
        img_exp = (img_exp * 255).astype('uint8')
        hist_exp = cv2.calcHist([img_exp], [0], None, [256], [0, 256])

# # 5. Ecualización adaptativa (CLAHE)
    def ecualizacion_adaptativa(self, img):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_clahe = clahe.apply(img)
        hist_clahe = cv2.calcHist([img_clahe], [0], None, [256], [0, 256])

# 6. Transformación Rayleigh (ajuste de escala)
    def transformacion_rayleigh(self, img):
        scale = 50  # Ajustar según necesidad
        rayleigh_cdf = 1 - np.exp(-(np.arange(256)*2)/(2(scale**2)))
        img_rayleigh = rayleigh_cdf[img] * 255
        img_rayleigh = img_rayleigh.astype('uint8')
        hist_rayleigh = cv2.calcHist([img_rayleigh], [0], None, [256], [0, 256])
