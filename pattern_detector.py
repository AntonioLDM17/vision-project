
import cv2
import numpy as np
from collections import deque
import time
from dice_reader_color import detect_dice


# RED: 2 -> YELLOW: 3 -> GREEN: 4 -> BLUE: 5
def pattern_test():

    # RED: 2
    color_to_detect = "red" 
    result = detect_dice(color_to_detect)
    print(f"Number of pips detected on {color_to_detect} dice: {result}")

    if result == 2:

        # YELLOW: 3
        color_to_detect = "yellow"
        result = detect_dice(color_to_detect)
        print(f"Number of pips detected on {color_to_detect} dice: {result}")

        if result == 3:

            # GREEN: 4
            color_to_detect = "green"
            result = detect_dice(color_to_detect)
            print(f"Number of pips detected on {color_to_detect} dice: {result}")

            if result == 4:

                # BLUE: 5
                color_to_detect = "blue"
                result = detect_dice(color_to_detect)
                print(f"Number of pips detected on {color_to_detect} dice: {result}")

                if result == 5:
                    
                    # Test passed
                    print("You passed the test!")
                    cv2.destroyAllWindows()
                else:
                    print("You failed the test!")
                    print("Restarting test...")
                    pattern_test()
            else:
                print("You failed the test!")
                print("Restarting test...")
                pattern_test()
        else:
            print("You failed the test!")
            print("Restarting test...")
            pattern_test()
    else:
        print("You failed the test!")
        print("Restarting test...")
        pattern_test()
        
if __name__ == "__main__":
    pattern_test()