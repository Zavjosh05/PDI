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
