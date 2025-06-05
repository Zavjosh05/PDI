import cv2
import numpy as np
import matplotlib.pyplot as plt  # Faltaba importar esto
from librerias.ProcesadorImagen import *  # Asegúrate de que esta ruta sea válida

# Cargar imagen en escala de grises
img = cv2.imread('coches.jpg', cv2.IMREAD_GRAYSCALE)

# Verificar que se haya cargado correctamente
if img is None:
    raise FileNotFoundError("No se encontró la imagen 'coches.jpg'.")

# Aplicar umbral adaptativo
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
smooth_hist = cv2.GaussianBlur(hist, (5,1), 0)
min_pos = np.argmin(smooth_hist[50:200]) + 50  # Evitar extremos
_, img_minhist = cv2.threshold(img, min_pos, 255, cv2.THRESH_BINARY)

# Mostrar imagen
plt.figure(figsize=(18, 10))  # Crear figura antes de mostrar
plt.subplot(4, 4, 1)
plt.imshow(img_minhist, cmap='gray')
plt.title('Umbral Adaptativo')
plt.axis('off')

plt.tight_layout()  # Organiza los subplots
plt.show()


