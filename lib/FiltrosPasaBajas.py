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