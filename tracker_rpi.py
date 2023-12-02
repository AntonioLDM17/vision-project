import numpy as np
import cv2
import sys
import time
import argparse
from collections import deque
from picamera2 import Picamera2

class ObjectTracker:
    def __init__(self, memory_size=64, video_source=None, target_color='red', min_size=10):
        self.memory_size = memory_size
        self.video_source = video_source
        self.target_color = target_color
        self.min_size = min_size
        self.memory = deque(maxlen=self.memory_size)
        self.initialize_camera()

    def initialize_camera(self):
        if not self.video_source:
            # Use Raspberry Pi camera
            self.camera = Picamera2()
            self.camera.preview_configuration.main.size = (640, 480)
            self.camera.preview_configuration.main.format = "RGB888"
            self.camera.preview_configuration.align()
            self.camera.configure("preview")
            self.camera.start()
            time.sleep(2.0)

    def capture_frame(self):
        frame = self.camera.capture_array()
        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (600, 400))
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        return hsv



    def create_mask(self, image):
        if self.target_color == 'red':
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

        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=3)
        return mask

    def identify_object(self, mask):
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            moments = cv2.moments(largest_contour)
            center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))

            if radius > self.min_size:
                return center, radius, (x, y)

        return None, None, None

    def visualize_frame(self, frame, center, radius, centroid):
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        cv2.circle(frame, (int(centroid[0]), int(centroid[1])), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

        for i in range(1, len(self.memory)):
            if self.memory[i - 1] is None or self.memory[i] is None:
                continue

            thickness = int(np.sqrt(self.memory_size / float(i + 1)) * 2.5)
            cv2.line(frame, self.memory[i - 1], self.memory[i], (0, 0, 255), thickness)

        frame = cv2.flip(frame, 1)
        return frame
    
    def track_single_frame(self):
        hsv = self.capture_frame()
        mask = self.create_mask(hsv)
        center, radius, centroid = self.identify_object(mask)

        if center is not None:
            self.memory.appendleft(center)
            return self.visualize_frame(hsv, center, radius, centroid)

        return cv2.flip(cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), 1)

    def track(self):
        while True:
            frame = self.track_single_frame()
            if frame is None:
                break
            cv2.imshow('Tracking Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_camera(self):
        cv2.destroyAllWindows()

    def __del__(self):
        self.close_camera()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--memory", type=int, default=64, help="maximum memory size")
    parser.add_argument("-t", "--target-color", type=str, default='red', help="color to track")
    parser.add_argument("-s", "--min-size", type=int, default=10, help="minimum size of the object to track")
    arguments = vars(parser.parse_args())

    tracker = ObjectTracker(arguments['memory'], None, arguments['target_color'], arguments['min_size'])
    tracker.track()