import cv2
import numpy as np
from collections import deque
import time
from picamera2 import Picamera2
from dice_reader_color_rpi import detect_dice


def pattern_test(picam):
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
                    pattern_test(picam)
            else:
                print("You failed the test!")
                print("Restarting test...")
                pattern_test(picam)
        else:
            print("You failed the test!")
            print("Restarting test...")
            pattern_test(picam)
    else:
        print("You failed the test!")
        print("Restarting test...")
        pattern_test(picam)



if __name__ == "__main__":
    picam = Picamera2()
    picam.preview_configuration.main.size = (640,480) #(1280, 720) Adjust this to the desired resolution
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
    pattern_test(picam)
    picam.stop()