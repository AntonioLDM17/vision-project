# Visión por Ordenador - Proyecto de Juego con Dados y Carreras

Este proyecto de visión por ordenador se centra en el uso de la librería cv2 de Python para el procesamiento y visualización de videos e imágenes, específicamente aplicado a la detección de colores, formas y blobs. El objetivo principal es implementar un juego de carreras con dados de colores utilizando una cámara, ya sea en Raspberry Pi o en un ordenador.

## 1. Descripción General del Proyecto

El proyecto consta de cinco funcionalidades principales:

### 1.1 Calibración de la Cámara

Se utiliza un conjunto de imágenes de un tablero de ajedrez para calibrar la cámara. Se detectan las esquinas del tablero, se refinan y se utiliza `cv2.calibrateCamera` para obtener la matriz intrínseca, los coeficientes de distorsión y la matriz extrínseca.

### 1.2 Detección de Patrones

Se implementa un script llamado `dice_reader_color` que utiliza la librería `cv2` para detectar y leer el número en un dado de colores. Se aplican máscaras de color para identificar diferentes colores y se utiliza un detector de blobs para identificar y contar los círculos en el dado.

### 1.3 Detección de Límites de Colores para Máscaras

Scripts adicionales ayudan a encontrar los valores HSV óptimos para las máscaras de color, adaptándolos según la iluminación y el dispositivo utilizado (Raspberry Pi o portátil).

### 1.4 Detector de Secuencias

El script `pattern_detector` utiliza la detección de patrones para verificar si el usuario muestra una secuencia específica de números en dados de colores. Se repite hasta que se completa la secuencia correctamente.

### 1.5 Tracker de los Dados

Se crea una clase `ObjectTracker` que utiliza técnicas de procesamiento de imágenes para realizar un seguimiento de objetos de cierto color a través de la cámara.

### 1.6 Juego

La última parte del proyecto es un juego de carreras con dados. Cuatro jugadores lanzan dados de colores, y el juego detecta el color del dado para avanzar las casillas correspondientes. El primero en llegar al final gana.

## 2. Instalación y Configuración

El archivo `main.py` proporciona la configuración principal para ejecutar el proyecto, incluyendo instrucciones para instalar y desinstalar librerías específicas para la Raspberry Pi.

Este resumen sirve como guía general para entender las funcionalidades del proyecto y cómo implementarlas. Se recomienda revisar los scripts individuales para detalles específicos y ajustes adicionales.
