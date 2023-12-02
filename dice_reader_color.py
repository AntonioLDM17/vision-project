import cv2
import numpy as np
from collections import deque

def detect_dice(color):
    min_threshold = 10
    max_threshold = 200
    min_area = 100
    min_circularity = 0.3
    min_inertia_ratio = 0.5

    cap = cv2.VideoCapture(0)
    cap.set(15, -4)

    counter = 0
    readings = deque([0, 0], maxlen=10)
    display = deque([0, 0], maxlen=10)

    while True:
        ret, im = cap.read()

        # Convert the frame to HSV color space for better color segmentation
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

        # Define color ranges based on the color parameter
        if color == "blue":
            lower_color = np.array([100, 50, 50])
            upper_color = np.array([130, 255, 255])
        elif color == "green":
            lower_color = np.array([40, 50, 50])
            upper_color = np.array([80, 255, 255])
        elif color == "yellow":
            lower_color = np.array([20, 100, 100])
            upper_color = np.array([40, 255, 255])
        elif color == "red":
            lower_color1 = np.array([0, 100, 100])
            upper_color1 = np.array([10, 255, 255])
            lower_color2 = np.array([160, 100, 100])
            upper_color2 = np.array([180, 255, 255])
            mask_color = cv2.inRange(hsv, lower_color1, upper_color1) | cv2.inRange(hsv, lower_color2, upper_color2)
        else:
            print("Invalid color parameter.")
            break

        if color != "red":
            mask_color = cv2.inRange(hsv, lower_color, upper_color)

        # Bitwise-AND the original image with the color mask
        result = cv2.bitwise_and(im, im, mask=mask_color)

        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.filterByCircularity = True
        params.filterByInertia = True
        params.minThreshold = min_threshold
        params.maxThreshold = max_threshold
        params.minArea = min_area
        params.minCircularity = min_circularity
        params.minInertiaRatio = min_inertia_ratio

        detector = cv2.SimpleBlobDetector_create(params)

        keypoints = detector.detect(result)

        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("Dice Reader", im_with_keypoints)

        if counter % 10 == 0:
            reading = len(keypoints)
            readings.append(reading)

            if readings[-1] == readings[-2] == readings[-3]:
                display.append(readings[-1])

            if display[-1] != display[-2] and display[-1] != 0:
                msg = f"{display[-1]}\n****"
                print(msg)
                return display[-1]

        counter += 1

        if cv2.waitKey(1) & 0xff == 27:
            break

    cv2.destroyAllWindows()

# Example usage:
color_to_detect = "red"  # Change this to the desired color ("blue", "green", "yellow", "red")
result = detect_dice(color_to_detect)
print(f"Number of pips detected on {color_to_detect} dice: {result}")

color_to_detect = "yellow"  # Change this to the desired color ("blue", "green", "yellow", "red")
result = detect_dice(color_to_detect)
print(f"Number of pips detected on {color_to_detect} dice: {result}")

color_to_detect = "green"  # Change this to the desired color ("blue", "green", "yellow", "red")
result = detect_dice(color_to_detect)
print(f"Number of pips detected on {color_to_detect} dice: {result}")


color_to_detect = "blue"  # Change this to the desired color ("blue", "green", "yellow", "red")
result = detect_dice(color_to_detect)
print(f"Number of pips detected on {color_to_detect} dice: {result}")