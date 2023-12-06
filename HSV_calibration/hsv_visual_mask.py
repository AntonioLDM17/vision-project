import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Define the base HSV values (adjust according to your needs)
hsv_min = np.array([15, 220, 100])
hsv_max = np.array([25, 255, 255])

# Main loop
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

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()