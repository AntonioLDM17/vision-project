import cv2
import numpy as np
import time

# Inicializar la cámara
cap = cv2.VideoCapture(0)


# Valores HSV iniciales (ajusta según tu necesidad)
hsv_min = np.array([60, 70, 20])
hsv_max = np.array([90, 255, 255])

while True:
    # Capturar un frame de la cámara
    ret, frame = cap.read()

    # Convertir el frame de BGR a HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crear una máscara utilizando los valores HSV
    mask = cv2.inRange(hsv_frame, hsv_min, hsv_max)

    # Aplicar la máscara al frame original
    result_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostrar el frame resultante
    cv2.imshow('Cámara con Máscara', result_frame)


    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()