import numpy as np
import cv2
import sys
import time
import argparse
from collections import deque
from picamera2 import Picamera2

class ObjectTracker:
    def __init__(self, memory_size=64, video_source=None, target_color='red', min_size=10, main=False, picam=None):
        # Initialize the ObjectTracker with default parameters or user-defined values.
        self.memory_size = memory_size
        self.video_source = video_source
        self.target_color = target_color
        self.min_size = min_size
        self.memory = deque(maxlen=self.memory_size)

        self.main = main
        self.picam = picam
        self.initialize_camera(main, picam)

    def initialize_camera(self, main, picam):
        # If the video source is specified, use it. Otherwise, initialize the Raspberry Pi camera.
        if not self.video_source and main==False:
            # Use Raspberry Pi camera
            self.camera = Picamera2()
            self.camera.preview_configuration.main.size = (640, 480)
            self.camera.preview_configuration.main.format = "RGB888"
            self.camera.preview_configuration.align()
            self.camera.configure("preview")
            self.camera.start()
            time.sleep(2.0)
        
        elif not self.video_source and main==True:
           #The camera is already initialized in the main
           # Use Raspberry Pi camera
            self.camera = picam
            

    def capture_frame(self):
        # Capture the frame
        frame = self.camera.capture_array()
        # Resize the frame
        frame = cv2.resize(frame, (600, 400))
        # Apply GaussianBlur to the frame
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        # Convert it to HSV
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        return hsv



    def create_mask(self, image):
        """
        Create a color mask based on the specified target color.
        Erosion and dilation are applied to reduce noise and improve accuracy.
        Return the resulting mask.
        """
        if self.target_color == 'red':
            # Define HSV range for red color (since it wraps around 0/180 degrees).
            lower_red_1 = np.array([0, 100, 20])
            upper_red_1 = np.array([10, 255, 255])
            lower_red_2 = np.array([160, 100, 20])
            upper_red_2 = np.array([179, 255, 255])
            mask = cv2.inRange(image, lower_red_1, upper_red_1) + cv2.inRange(image, lower_red_2, upper_red_2)

        elif self.target_color == 'blue':
            lower_blue = np.array([100, 100, 20])
            upper_blue = np.array([120, 255, 255])
            mask = cv2.inRange(image, lower_blue, upper_blue)

        elif self.target_color == 'green':
            lower_green = np.array([45, 100, 20])
            upper_green = np.array([76, 255, 255])
            mask = cv2.inRange(image, lower_green, upper_green)

        elif self.target_color == 'yellow':
            lower_yellow = np.array([20, 100, 20])
            upper_yellow = np.array([40, 255, 255])
            mask = cv2.inRange(image, lower_yellow, upper_yellow)
        
        elif self.target_color == 'purple':
            lower_purple = np.array([130, 100, 20])
            upper_purple = np.array([150, 255, 255])
            mask = cv2.inRange(image, lower_purple, upper_purple)

        else:
            raise ValueError('Invalid color. Choose from red, blue, green, purple or yellow.')

        # Apply erosion and dilation to the mask
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=3)
        return mask


    def identify_object(self, mask):
        """
        Identify the object in the mask using contours and return its center, radius, and centroid.
        If the object size is larger than the specified minimum size, return the values.
        Otherwise, return None.
        """

        #Find the contours of the mask
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # If there are contours
        if len(contours) > 0:
            #Selects the contour with the biggest area
            largest_contour = max(contours, key=cv2.contourArea)
            #Find the minimum size circle that can enclose the largest contour
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            # Find the moments of the largest contour
            moments = cv2.moments(largest_contour)
            # Find the centroid of the largest contour
            center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))

            # Return the center, radius, and centroid if the radius is larger than the minimum size
            if radius > self.min_size:
                return center, radius, (x, y)

        return None, None, None

    def visualize_frame(self, frame, center, radius, centroid):
        """
        Visualize the frame with circles indicating the object's position, trajectory lines, and flip horizontally.
        """

        # Convert the frame from HSV to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        # Draw the circle and centroid on the frame
        cv2.circle(frame, (int(centroid[0]), int(centroid[1])), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # Draw the trajectory lines
        for i in range(1, len(self.memory)):
            if self.memory[i - 1] is None or self.memory[i] is None:
                continue
            
            # Compute the thickness of the line and draw the connecting lines
            thickness = int(np.sqrt(self.memory_size / float(i + 1)) * 2.5)
            cv2.line(frame, self.memory[i - 1], self.memory[i], (0, 0, 255), thickness)

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        return frame

    def track_single_frame(self):
        """
        Track a single frame by capturing it, creating a mask, 
        identifying the object, and visualizing the result.
        """

        # Capture the frame
        hsv = self.capture_frame()
        # If there is no frame, return None
        if hsv is None:
            return None
        # Create a mask
        mask = self.create_mask(hsv)
        # Identify the object
        center, radius, centroid = self.identify_object(mask)

        # If the object is identified, append the center to the memory
        if center is not None:
            self.memory.appendleft(center)
            # Visualize the frame
            return self.visualize_frame(hsv, center, radius, centroid)
        # If the object is not identified, return the frame as is
        return cv2.flip(cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), 1)

    def track(self):
        # Track the object indefinitely until the user presses 'q'
        while True:
            frame = self.track_single_frame()
            if frame is None:
                break
            cv2.imshow('Tracking Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_camera(self):
        # Release the camera and close all windows
        self.camera.release()
        cv2.destroyAllWindows()

    def __del__(self):
        # Destructor to close the camera when the ObjectTracker object is deleted
        self.close_camera()

def tracking_main(color_to_track, main, picam):
    # Parse the arguments and create an ObjectTracker object with the specified parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--memory", type=int, default=64, help="maximum memory size")
    parser.add_argument("-t", "--target-color", type=str, default=color_to_track, help="color to track")
    parser.add_argument("-s", "--min-size", type=int, default=10, help="minimum size of the object to track")
    arguments = vars(parser.parse_args())

    # Initialize the ObjectTracker object and track the object
    tracker = ObjectTracker(arguments['memory'], None, arguments['target_color'], arguments['min_size'], main=main, picam=picam)
    tracker.track()

if __name__ == "__main__":
    tracking_main(color_to_track="green", main = False, picam=None) # Change this to the color you want to track ("blue", "green", "yellow", "red", "purple")