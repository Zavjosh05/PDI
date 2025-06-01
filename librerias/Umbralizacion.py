import cv2
import numpy as np
from skimage.filters import *
from librerias.ProcesadorImagen import *

class Umbralizacion:

    def __init__(self):
        self.procesador = ProcesadorImagen()
# 1. Umbral por Media
    def umbral_media(self, img):
        img_gray = self.procesador.convertir_a_grises(img)
        mean_val = np.mean(img_gray)
        _, img_mean = cv2.threshold(img_gray, mean_val, 255, cv2.THRESH_BINARY)
        return img_mean

# 2. Método de Otsu
    def metodo_otsu(self, img):
        img_gray = self.procesador.convertir_a_grises(img)
        otsu_thresh, img_otsu = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img_otsu

# 3. Multiumbralización (Otsu multinivel)
    def multiumbralizacion(self, img):
        img_gray = self.procesador.convertir_a_grises(img)
        thresholds = threshold_multiotsu(img_gray, classes=3)
        regions = np.digitize(img_gray, bins=thresholds)
        img_multi = np.uint8(regions * (255/2))  # Escalar para visualización
        return img_multi

# 4. Entropía de Kapur (similar a Yen)
    def entropia_kapur(self, img):
        img_gray = self.procesador.convertir_a_grises(img=img)
        kapur_thresh = threshold_yen(img_gray)
        _, img_kapur = cv2.threshold(img_gray, kapur_thresh, 255, cv2.THRESH_BINARY)
        return img_kapur

# 5. Umbral por Banda (rango de intensidades)
    def umbral_por_banda(self, img):
        img_gray = self.procesador.convertir_a_grises(img)
        lower = 100
        upper = 200
        img_band = cv2.inRange(img_gray, lower, upper)
        return img_band

# 6. Umbral Adaptativo
    def umbral_adaptativo(self, img):
        img_gray = self.procesador.convertir_a_grises(img)
        img_adapt = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 11, 2)
        return img_adapt

# 7. Mínimo del Histograma (método de Prewitt modificado)
    def minimo_del_histograma(self, img):
        img_gray = self.procesador.convertir_a_grises(img)
        hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
        smooth_hist = cv2.GaussianBlur(hist, (5,1), 0)
        min_pos = np.argmin(smooth_hist[50:200]) + 50  # Evitar extremos
        _, img_minhist = cv2.threshold(img, min_pos, 255, cv2.THRESH_BINARY)
        return img_minhist

    def filtro_Robert(self, img):

        imagen_nueva = self.procesador.convertir_a_grises(img)
         
        # Definir el kernel de Robert
        kernel_roberts_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
        kernel_roberts_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        # Aplicar el filtro
        bordes_roberts_x = cv2.filter2D(imagen_nueva, -1, kernel_roberts_x)
        bordes_roberts_y = cv2.filter2D(imagen_nueva, -1, kernel_roberts_y)
        imagen_bordes_roberts = cv2.addWeighted(bordes_roberts_x, 0.5, bordes_roberts_y, 0.5, 0)

        if(imagen_bordes_roberts.any()): 
            print("obtencion de bordes exitosas")
        return imagen_bordes_roberts

# Función para componentes conexas con vecindad-8 (implementación manual ajskasjka equisde)
    def connected_components_8neighbors(binary_img):
        labeled = np.zeros_like(binary_img, dtype=np.int32)
        current_label = 1
        rows, cols = binary_img.shape
    
    # Direcciones de los 8 vecinos
    def vecindad_8(self,img):
        directions = [(-1,-1), (-1,0), (-1,1),
                    (0,-1),          (0,1),
                    (1,-1),  (1,0), (1,1)]
        
        for i in range(rows):
            for j in range(cols):
                if binary_img[i,j] == 255 and labeled[i,j] == 0:  # Píxel no etiquetado
                    # BFS para etiquetar componente conexa
                    queue = deque()
                    queue.append((i,j))
                    labeled[i,j] = current_label
                    
                    while queue:
                        x, y = queue.popleft()
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < rows and 0 <= ny < cols and 
                                binary_img[nx,ny] == 255 and labeled[nx,ny] == 0):
                                labeled[nx,ny] = current_label
                                queue.append((nx,ny))
                    
                    current_label += 1
        return labeled, current_label - 1

# Aplicar componentes conexas
    def componentes_conexas(self, img):
        labeled_img, num_objects = connected_components_8neighbors(img)
        return labeled_img

# Colorear componentes para visualización perrila
    def componentes_visualizacion_perrila(self, img):
        colored_components = np.zeros((*labeled_img.shape, 3), dtype=np.uint8)
        for label in range(1, num_objects + 1):
            color = tuple(np.random.randint(0, 255, 3).tolist())
            colored_components[labeled_img == label] = color