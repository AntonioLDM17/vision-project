import cv2
import numpy as np
import time

# Initialize the camera
cap = cv2.VideoCapture(0)

# Define the update interval (in seconds) and the last update time
tick = 0.5
last_tick = time.time()

# Define the initial HSV values º(adjust according to your needs)
hsv_min = np.array([0, 100, 100])
hsv_max = np.array([10, 255, 255])

while True:

    # Capture a frame from the camera
    ret, frame = cap.read()

    # Convert the frame from BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask using the HSV values
    mask = cv2.inRange(hsv_frame, hsv_min, hsv_max)

    # Apply the mask to the original frame
    result_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the resulting frame (with mask)
    cv2.imshow('Cámara con Máscara', result_frame)

    # Check if it is time to update the HSV values
    if time.time() - last_tick > tick:
        # Update the HSV values
        hsv_min[0] += 5  
        if hsv_min[0] >= 180:
            hsv_min[0] = 0  
        hsv_max[0] = hsv_min[0] + 10  
        
        # Print the new HSV values
        print(f"Nuevo rango HSV: {hsv_min} a {hsv_max}")

        # Update the last update time
        last_tick = time.time()

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
