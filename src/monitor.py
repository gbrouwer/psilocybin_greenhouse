import time
import cv2
import numpy as np
import imageio
import board
import adafruit_bh1750
from datetime import datetime
from sense_hat import SenseHat

#---------------------------------------------------------------
if __name__ == '__main__':

    #open Sensor
    i2c = board.I2C()
    sensor = adafruit_bh1750.BH1750(i2c)

    #Loop
    while True:

        #Start Image Capture 1
        cap = cv2.VideoCapture(0)
        time.sleep(1.0)
        success, image = cap.read()
        if (success == True):
            filename = str(datetime.now())
            filename = filename.replace(' ', '-').split('.')[0]
            filename = filename.replace(':', '-') + '.png'
            filename = '/home/pi/Code/psilocybin_greenhouse/data/camera1/' + filename
            imageio.imwrite(filename, image)

        #Stop
        cap.release()
        time.sleep(1.0)

        #Start Image Capture 2
        cap = cv2.VideoCapture(2)
        time.sleep(1.0)
        success, image = cap.read()
        if (success == True):
            filename = str(datetime.now())
            filename = filename.replace(' ', '-').split('.')[0]
            filename = filename.replace(':', '-') + '.png'
            filename = '/home/pi/Code/psilocybin_greenhouse/data/camera2/' + filename
            imageio.imwrite(filename, image)

        #Stop
        cap.release()
        time.sleep(1.0)

        #Read Light Sensor for the remaining time
        for i in range(56):

            #Read
            print(sensor.lux)
            lux = sensor.lux
            time.sleep(1.0)

            #Write
            current_time = datetime.now()
            filename = str(current_time)
            filename = filename.replace(' ', '-').split('.')[0]
            filename = filename.replace(':', '-')
            filename = '/home/pi/Code/psilocybin_greenhouse/data/lux/' + filename[:10] + '.csv'
            with open(filename, 'a') as f:

                #Store
                measurements = np.zeros(7)
                measurements[0] = lux
                measurements[1] = current_time.year
                measurements[2] = current_time.month
                measurements[3] = current_time.day
                measurements[4] = current_time.hour
                measurements[5] = current_time.minute
                measurements[6] = current_time.second

                #Write
                writestr = ''
                for j in range(7):
                    if (j < 1):
                        writestr = writestr + str(measurements[j]) + ','
                    else:
                        writestr = writestr + str(int(measurements[j])) + ','
                writestr = writestr[:-1] + '\n'
                f.write(writestr)




        # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        # cap.set(cv2.CAP_PROP_EXPOSURE, 10.0)
        # cap.set(cv2.CAP_PROP_BRIGHTNESS, 40.0)
        # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        # cap.set(cv2.CAP_PROP_FOCUS, 300)
