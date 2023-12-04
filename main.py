# First we start by importing the necessary libraries
import time
import sys
import subprocess

RaspberryPi = True  # This variable will be used to determine if we are using a Raspberry Pi or a PC

if RaspberryPi == False:
    # Now we will import the files that contain the functions we will use
    import camera_calibration as cc  # This is the file that contains the camera calibration functions
    import tracker_webcam_pc as tw  # This is the file that contains the object tracking functions
    import dice_reader_color as drp  # This is the file that contains the dice recognition functions
    import pattern_detector as pd  # This is the file that contains the sequence recognition functions
    import game as gm  # This is the file that contains the game functions

if RaspberryPi == True:
    # Now we will import the files that contain the functions we will use
    import camera_calibration as cc  # This is the file that contains the camera calibration functions
    import tracker_rpi as tw  # This is the file that contains the object tracking functions
    import dice_reader_color_rpi as drp  # This is the file that contains the dice recognition functions
    import pattern_detector_rpi as pd  # This is the file that contains the sequence recognition functions
    import game as gm  # This is the file that contains the game functions

# Now we will begin with camera calibration
print("Camera calibration\n")
time.sleep(1.0)

if RaspberryPi == False:
    cc.calibration_camera()
if RaspberryPi == True:
    # There are some issues with the opencv-python package in the Raspberry Pi, so we will uninstall it and install the opencv-python-headless package
    subprocess.run(["pip", "uninstall", "opencv-python"])
    subprocess.run(["pip", "install", "opencv-python-headless"])
    cc.calibration_camera()
    # After the calibration, we will reinstall the opencv-python package because it is needed for the rest of the program
    subprocess.run(["pip", "uninstall", "opencv-python-headless"])
    subprocess.run(["pip", "install", "opencv-python"])

print("\nCamera calibration completed\n")

# After calibration, we will start with the pattern recognition
print("\nPattern recognition\n")
time.sleep(1.0)
if RaspberryPi == False:
    picam, result = drp.dice_detection(color_to_detect='red')
if RaspberryPi == True:
    picam, result = drp.dice_detection(color_to_detect='red', picam=None)
print("Pattern recognition completed\n")

# After pattern recognition, now it is time to detect the sequence of dices
print("\nSequence recognition\n")
time.sleep(1.0)
print("For this test, you will need to place the dices in a specific order and show the correct number of pips for each dice.\n")
time.sleep(2.0)
if RaspberryPi == False:
    pd.pattern_test()
if RaspberryPi == True:
    pd.pattern_test(picam)
print("Sequence recognition completed\n")

# Now let's begin with the object tracking
print("\nObject tracking\n")
time.sleep(1.0)
print("Show an object to the camera and it will follow it.\n")
print("Press 'q' to stop the object tracking.\n")
if RaspberryPi == False:
    tw.tracking_main(color_to_track='green')
if RaspberryPi == True:
    tw.tracking_main(color_to_track='green', main=True, picam=picam)
print("Object tracking completed\n")

# After everything has been checked, we will now proceed to play the game
print("\nGame time\n")
time.sleep(1.0)
gm.game_main(picam = picam, RaspberryPi=RaspberryPi)
print("\nGame completed\n")
time.sleep(1.0)
print("Thank you for playing!")
sys.exit(0)
