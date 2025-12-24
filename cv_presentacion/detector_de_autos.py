from ultralytics import YOLO
import numpy as np
import cv2
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("Cars Moving On Road Stock Footage - Free Download.mp4")

def add_salt_pepper_noise(image, prob = 0.1):
    noisy = image.copy()
    black = 0
    white = 255
    probs = np.random.rand(*image.shape[:2])
    noisy[probs < prob/2] = black
    noisy[probs > 1 - prob/2] = white
    return noisy

def detect_and_draw(frame, color=(0, 255, 0)):
    results = model(frame)[0]
    detections = [det for det in results.boxes.data if int(det[5]) == 2]

    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(frame, f'Car {conf:.2f}', (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame, len(detections)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 360))
    noisy = add_salt_pepper_noise(frame.copy())
    filtered = cv2.medianBlur(noisy.copy(), 5)

    noisy_detected, count_noisy = detect_and_draw(noisy, color=(0, 0, 255))
    filtered_detected, count_filtered = detect_and_draw(filtered, color=(0, 255, 0))
    combined = cv2.hconcat([noisy_detected, filtered_detected])

    cv2.putText(combined, f'Ruido: {count_noisy} autos', (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(combined, f'Filtrado: {count_filtered} autos', (660, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Sal y Pimienta vs Promediador Pesado", combined)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
