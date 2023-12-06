import sys
import subprocess
import time

# General imports
import camera_calibration as cc  # This is the file that contains the camera calibration functions
import game as gm  # This is the file that contains the game functions


def rpi_main(RaspberryPi):

    # Import the Raspberry Pi specific files

    # Raspberry Pi imports
    import tracker_rpi as twi  # This is the file that contains the object tracking functions
    import dice_reader_color_rpi as drpi  # This is the file that contains the dice recognition functions
    import pattern_detector_rpi as pdi  # This is the file that contains the sequence recognition functions
    # 1. Calibration

    print("Camera calibration\n")
    time.sleep(1.0)

    # There are some issues with the opencv-python package in the Raspberry Pi, so we will uninstall it and install the opencv-python-headless package
    subprocess.run(["pip", "uninstall", "opencv-python"])
    subprocess.run(["pip", "install", "opencv-python-headless"])

    # Calibrate the camera
    cc.calibration_camera()

    # After the calibration, we will reinstall the opencv-python package because it is needed for the rest of the program
    subprocess.run(["pip", "install", "opencv-python"])

    print("\nCamera calibration completed\n")


    # 2. Pattern detection

    print("\nPattern recognition\n")
    time.sleep(1.0)

    picam, result = drpi.dice_detection(color_to_detect='red', picam=None)

    print("\Recognition works\n")
    print("For this test, you will need to place the dices in a specific order and show the correct number of pips for each dice.\n")
    time.sleep(2.0)

    pdi.pattern_test(picam)
    print("Sequence recognition completed\n")


    # 3. Object tracking

    print("\nObject tracking\n")
    time.sleep(1.0)

    print("Show an object to the camera and it will follow it.\n")
    print("Press 'q' to stop the object tracking.\n")

    twi.tracking_main(color_to_track='green', main=True, picam=picam)
    print("Object tracking completed\n")


    # 4. Game

    print("\nGame time\n")
    time.sleep(1.0)
    gm.game_main(picam = picam, RaspberryPi=RaspberryPi)
    print("\nGame completed\n")
    time.sleep(1.0)
    print("Thank you for playing!")
    sys.exit(0)



def camera_main(RaspberryPi):

    # Import the camera specific files
    import tracker_webcam_pc as tw  # This is the file that contains the object tracking functions
    import dice_reader_color as drp  # This is the file that contains the dice recognition functions
    import pattern_detector as pd  # This is the file that contains the sequence recognition functions

    # 1. Calibration

    print("Camera calibration\n")
    time.sleep(1.0)

    # Calibrate the camera
    cc.calibration_camera()

    print("\nCamera calibration completed\n")


    # 2. Pattern detection

    print("\nPattern recognition\n")
    time.sleep(1.0)

    picam, result = drp.dice_detection(color_to_detect='red')

    print("\Recognition works\n")
    print("For this test, you will need to place the dices in a specific order and show the correct number of pips for each dice.\n")
    time.sleep(2.0)

    pd.pattern_test()
    print("Sequence recognition completed\n")


    # 3. Object tracking

    print("\nObject tracking\n")
    time.sleep(1.0)

    print("Show an object to the camera and it will follow it.\n")
    print("Press 'q' to stop the object tracking.\n")

    tw.tracking_main(color_to_track='green')
    print("Object tracking completed\n")
    

    # 4. Game

    print("\nGame time\n")
    time.sleep(1.0)

    gm.game_main(picam = picam, RaspberryPi=RaspberryPi)

    print("\nGame completed\n")
    print("Thank you for playing!")
    time.sleep(1.0)
    sys.exit(0)


if __name__ == "__main__":

    RaspberryPi = input('Are you using Raspberry Pi? (y/n): ')

    if  RaspberryPi == 'y':
        RaspberryPi = True
    elif RaspberryPi == 'n':
        RaspberryPi = False
    else:
        print('Invalid input')
        sys.exit()

    if RaspberryPi:
        rpi_main(RaspberryPi=RaspberryPi)
    else:
        camera_main(RaspberryPi=RaspberryPi)
