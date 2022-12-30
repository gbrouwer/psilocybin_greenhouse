import time
import cv2
import numpy as np
import imageio
from datetime import datetime
from sense_hat import SenseHat

#---------------------------------------------------------------
if __name__ == '__main__':

    # # Parameters
    # black = (0, 0, 0)
    # white = (250, 250, 250)
    # sense = SenseHat()
    # sense.clear(black)
    # sense.set_rotation(180)
    [0,2,]
    #Loop
    #while True:
    for i in range(2):

        # Start Video Capture
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, 10.0)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 40.0)
        # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        # cap.set(cv2.CAP_PROP_FOCUS, 300)
        time.sleep(1.0)

        #Record
        success, image = cap.read()
        if (success == True):

            #Save
            filename = str(datetime.now())
            filename = filename.replace(' ', '-').split('.')[0]
            filename = filename.replace(':', '-') + '.png'
            filename = '/home/pi/Code/psilocybin_greenhouse/data/camera1/' + filename
            imageio.imwrite(filename, image)

        #Sleep until the next image needs to be captured
        time.sleep(2.0)

        #Stop
        cap.release()


        # Start Video Capture
        cap = cv2.VideoCapture(2)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(cv2.CAP_PROP_EXPOSURE, 10.0)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 40.0)
        # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        # cap.set(cv2.CAP_PROP_FOCUS, 300)
        time.sleep(1.0)

        #Record
        success, image = cap.read()
        if (success == True):

            #Save
            filename = str(datetime.now())
            filename = filename.replace(' ', '-').split('.')[0]
            filename = filename.replace(':', '-') + '.png'
            filename = '/home/pi/Code/psilocybin_greenhouse/data/camera2/' + filename
            imageio.imwrite(filename, image)

        #Interval (1 minute - 10 seconds)
        time.sleep(56.0)

        #Stop
        cap.release()


