#Ajustes de brillo

# Filtros pasa-bajas
# 1. Filtro promediador (box blur)
kernel_size = 5
# img_promediador = cv2.blur(img_rayleigh, (kernel_size, kernel_size))

# 2. Filtro promediador pesado (weighted average)
# kernel_pesado = np.array([[1, 2, 1],
#                           [2, 4, 2],
#                           [1, 2, 1]]) / 16
# img_pesado = cv2.filter2D(img_rayleigh, -1, kernel_pesado)

# 3. Filtro mediana
img_mediana = cv2.medianBlur(img_rayleigh, kernel_size)

# 4. Filtro moda (implementación manual)
def mode_filter(img, size=3):
    pad = size//2
    padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REFLECT)
    result = np.zeros_like(img)
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+size, j:j+size]
            values, counts = np.unique(window, return_counts=True)
            result[i,j] = values[np.argmax(counts)]
    return result

img_moda = mode_filter(img_rayleigh, 5)

# 5. Filtro bilateral
img_bilateral = cv2.bilateralFilter(img_rayleigh, 9, 75, 75)

# 6. Filtros máximo y mínimo
#img_maximo = cv2.dilate(img_rayleigh, np.ones((kernel_size,kernel_size)))
img_minimo = cv2.erode(img_rayleigh, np.ones((kernel_size,kernel_size)))

# 7. Filtro gaussiano
#img_gaussiano = cv2.GaussianBlur(img_rayleigh, (kernel_size, kernel_size), 0)

# filtos pasa-altas
# 1. Operador Robinson (8 direcciones)
def robinson_filter(img):
    kernels = [
        np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),  # Norte
        np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]),   # Noreste
        np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),   # Este
        np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]]),   # Sureste
        np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]),   # Sur
        np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]]),   # Suroeste
        np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),   # Oeste
        np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])    # Noroeste
    ]
    magnitude = np.zeros_like(img, dtype=np.float32)
    for kernel in kernels:
        filtered = cv2.filter2D(img, cv2.CV_32F, kernel)
        magnitude = np.maximum(magnitude, np.abs(filtered))
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

img_robinson = robinson_filter(img)

# 2. Operador Robert
roberts_x = np.array([[1, 0], [0, -1]])
roberts_y = np.array([[0, 1], [-1, 0]])
roberts_x_img = cv2.filter2D(img, cv2.CV_16S, roberts_x)
roberts_y_img = cv2.filter2D(img, cv2.CV_16S, roberts_y)
img_robert = cv2.convertScaleAbs(cv2.addWeighted(roberts_x_img, 0.5, roberts_y_img, 0.5, 0))

# 3. Operador Prewitt
prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
prewitt_x_img = cv2.filter2D(img, cv2.CV_16S, prewitt_x)
prewitt_y_img = cv2.filter2D(img, cv2.CV_16S, prewitt_y)
img_prewitt = cv2.convertScaleAbs(cv2.addWeighted(prewitt_x_img, 0.5, prewitt_y_img, 0.5, 0))

# 4. Operador Sobel
sobel_x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize=3)
sobel_y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize=3)
img_sobel = cv2.convertScaleAbs(cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0))

# 5. Operador Kirsch (8 direcciones)
def kirsch_filter(img):
    kernels = [
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),   # Norte
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]),    # Noreste
        np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),    # Este
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),    # Sureste
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),    # Sur
        np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),    # Suroeste
        np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),    # Oeste
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]])     # Noroeste
    ]
    magnitude = np.zeros_like(img, dtype=np.float32)
    for kernel in kernels:
        filtered = cv2.filter2D(img, cv2.CV_32F, kernel)
        magnitude = np.maximum(magnitude, np.abs(filtered))
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

img_kirsch = kirsch_filter(img)

# 6. Detector Canny
img_canny = cv2.Canny(img, 100, 200)

# 7. Operador Laplaciano
laplacian = cv2.Laplacian(img, cv2.CV_16S, ksize=3)
img_laplacian = cv2.convertScaleAbs(laplacian)

# umbralización
# 1. Umbral por Media
mean_val = np.mean(img)
_, img_mean = cv2.threshold(img, mean_val, 255, cv2.THRESH_BINARY)

# 2. Método de Otsu
otsu_thresh, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 3. Multiumbralización (Otsu multinivel)
thresholds = threshold_multiotsu(img, classes=3)
regions = np.digitize(img, bins=thresholds)
img_multi = np.uint8(regions * (255/2))  # Escalar para visualización

# 4. Entropía de Kapur (similar a Yen)
kapur_thresh = threshold_yen(img)
_, img_kapur = cv2.threshold(img, kapur_thresh, 255, cv2.THRESH_BINARY)

# 5. Umbral por Banda (rango de intensidades)
lower = 100
upper = 200
img_band = cv2.inRange(img, lower, upper)

# 6. Umbral Adaptativo
img_adapt = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 11, 2)

# 7. Mínimo del Histograma (método de Prewitt modificado)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
smooth_hist = cv2.GaussianBlur(hist, (5,1), 0)
min_pos = np.argmin(smooth_hist[50:200]) + 50  # Evitar extremos
_, img_minhist = cv2.threshold(img, min_pos, 255, cv2.THRESH_BINARY)

# Función para componentes conexas con vecindad-8 (implementación manual ajskasjka equisde)
def connected_components_8neighbors(binary_img):
    labeled = np.zeros_like(binary_img, dtype=np.int32)
    current_label = 1
    rows, cols = binary_img.shape
    
    # Direcciones de los 8 vecinos
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
labeled_img, num_objects = connected_components_8neighbors(img)

# Colorear componentes para visualización perrila
colored_components = np.zeros((*labeled_img.shape, 3), dtype=np.uint8)
for label in range(1, num_objects + 1):
    color = tuple(np.random.randint(0, 255, 3).tolist())
    colored_components[labeled_img == label] = color