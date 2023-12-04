import cv2
import numpy as np
import time

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Definir el intervalo de actualización (en segundos)
intervalo_actualizacion = 0.5
ultimo_tiempo_actualizacion = time.time()

# Valores HSV iniciales (ajusta según tu necesidad)
hsv_min = np.array([60, 0, 50])
hsv_max = np.array([90, 30, 255])

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

    # Comprobar si es el momento de actualizar los valores HSV
    if time.time() - ultimo_tiempo_actualizacion > intervalo_actualizacion:
        # Actualizar los valores HSV
        hsv_min[1] += 5  # Modificar el valor H mínimo
        if hsv_min[1] >= 255:
            hsv_min[1] = 0  # Reiniciar si supera 180
        hsv_max[1] = hsv_min[1] + 30  # Actualizar el valor H máximo

        # Imprimir los nuevos valores HSV
        print(f"Nuevo rango HSV: {hsv_min} a {hsv_max}")

        # Actualizar el tiempo de la última actualización
        ultimo_tiempo_actualizacion = time.time()

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
