import cv2
import numpy as np
from collections import deque

# Function to detect the number of pips on a dice of a given color (blue, green, yellow, red)
def detect_dice(color):

    # Define the parameters for the blob detector
    min_threshold = 10 
    max_threshold = 200
    min_area = 100
    min_circularity = 0.3
    min_inertia_ratio = 0.5

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    cap.set(15, -4) # Set the exposure of the camera

    # Initialize the variables for the detection algorithm
    counter = 0 # Counter to handle FPS
    # Lists to track the number of pips
    readings = deque([0, 0], maxlen=10) 
    display = deque([0, 0], maxlen=10)  

    # Main loop
    while True:

        # Capture a frame from the camera
        ret, im = cap.read()

        # Convert the frame from BGR to HSV color space for better color segmentation
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

        # Define color ranges based on the color parameter (iPhone best params)
        if color == "blue":

            lower_color = np.array([100, 50, 50])
            upper_color = np.array([130, 255, 255])

        elif color == "green":

            lower_color = np.array([60, 70, 20])
            upper_color = np.array([90, 255, 255])

        elif color == "yellow":

            lower_color = np.array([15, 220, 100])
            upper_color = np.array([25, 255, 255])

        elif color == "red":

            lower_color1 = np.array([0, 70, 100])
            upper_color1 = np.array([10, 255, 255])
            lower_color2 = np.array([160, 70, 100])
            upper_color2 = np.array([180, 255, 255])

            # Red is a special case, since it wraps around the color space
            mask_color = cv2.inRange(hsv, lower_color1, upper_color1) | cv2.inRange(hsv, lower_color2, upper_color2)

        else:

            print("Invalid color parameter.")
            break

        # Create a mask using the HSV values
        if color != "red":
            mask_color = cv2.inRange(hsv, lower_color, upper_color)

        # Apply the mask to the original frame
        result = cv2.bitwise_and(im, im, mask=mask_color)

        # Create the blob detector and detect blobs
        params = cv2.SimpleBlobDetector_Params() 
        params.filterByArea = True 
        params.filterByCircularity = True
        params.filterByInertia = True
        params.minThreshold = min_threshold
        params.maxThreshold = max_threshold
        params.minArea = min_area
        params.minCircularity = min_circularity
        params.minInertiaRatio = min_inertia_ratio

        # Create a detector with the parameters and detect blobs (pips) in the image
        detector = cv2.SimpleBlobDetector_create(params)

        # Detect blobs
        keypoints = detector.detect(result)

        # Draw blobs on our image as red circles
        im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


        '''i2 = cv2.bitwise_and(im_with_keypoints, im_with_keypoints, mask=mask_color)
        cv2.imshow("Dice Reader", i2)'''
        
        # Show the resulting frame (with blobs)
        cv2.imshow("Dice Reader", im_with_keypoints)

        # Update the display and readings queues and detect the number of pips 
        if counter % 10 == 0: # Enter this block every 10 frames
            reading = len(keypoints) # Counts keypoints (pips)
            readings.append(reading) # Save this frame's reading

            # If the 3 most recent readings are equal, then we have a reliable reading
            if readings[-1] == readings[-2] == readings[-3]: 
                display.append(readings[-1])

            # If the last valid reading has changed, and it's not zero, print it
            if display[-1] != display[-2] and display[-1] != 0:
                msg = f"{display[-1]}\n****"
                print(msg)
                return display[-1]

        counter += 1

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xff == 27:
            break

    cv2.destroyAllWindows()


def dice_detection(color_to_detect):
    # Example usage:
    result = detect_dice(color_to_detect)
    print(f"Number of pips detected on {color_to_detect} dice: {result}")
    return None, result

if __name__ == "__main__":
    dice_detection(color_to_detect="red") # Change this to the desired color ("blue", "green", "yellow", "red")