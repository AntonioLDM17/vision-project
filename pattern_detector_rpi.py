import cv2
import numpy as np
from collections import deque
import time
from picamera2 import Picamera2

def detect_dice(color, picam):
    min_threshold = 10
    max_threshold = 200
    min_area = 100
    min_circularity = 0.3
    min_inertia_ratio = 0.5

    counter = 0
    readings = deque([0, 0], maxlen=10)
    display = deque([0, 0], maxlen=10)

    while True:
        frame = picam.capture_array()

        # Convert the frame to BGR format (OpenCV uses BGR)
        # im = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        im = frame

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

def pattern_test_0(picam):
    # Example usage:
    color_to_detect = "red"  # Change this to the desired color ("blue", "green", "yellow", "red")
    result = detect_dice(color_to_detect, picam)
    print(f"Number of pips detected on {color_to_detect} dice: {result}")
    if result == 2:
        color_to_detect = "yellow"  # Change this to the desired color ("blue", "green", "yellow", "red")
        result = detect_dice(color_to_detect, picam)
        print(f"Number of pips detected on {color_to_detect} dice: {result}")
        if result == 3:
            color_to_detect = "green"
            result = detect_dice(color_to_detect, picam)
            print(f"Number of pips detected on {color_to_detect} dice: {result}")
            if result == 4:
                color_to_detect = "blue"
                result = detect_dice(color_to_detect, picam)
                print(f"Number of pips detected on {color_to_detect} dice: {result}")
                if result == 5:
                    print("You passed the test!")
                    cv2.destroyAllWindows()
                else:
                    print("You failed the test!")
                    print("Restarting test...")
                    pattern_test_0(picam)
            else:
                print("You failed the test!")
                print("Restarting test...")
                pattern_test_0(picam)
        else:
            print("You failed the test!")
            print("Restarting test...")
            pattern_test_0(picam)
    else:
        print("You failed the test!")
        print("Restarting test...")
        pattern_test_0(picam)

def pattern_test(picam):

    pattern_test_0(picam)

if __name__ == "__main__":
    picam = Picamera2()
    picam.preview_configuration.main.size = (640,480) #(1280, 720) Adjust this to the desired resolution
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    pattern_test(picam)
    picam.stop()