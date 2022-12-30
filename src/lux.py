import sys, getopt
import numpy as np
from datetime import datetime
import time
import math
import board
import adafruit_bh1750

#------------------------------------------------------------------------
if __name__ == '__main__':

    #Init
    i2c = board.I2C()
    sensor = adafruit_bh1750.BH1750(i2c)

    #loop
    while True:

        #Get Data and Date
        current_time = datetime.now()
        measurements = np.zeros(7)
        measurements[0] = sensor.lux
        measurements[1] = current_time.year
        measurements[2] = current_time.month
        measurements[3] = current_time.day
        measurements[4] = current_time.hour
        measurements[5] = current_time.minute
        measurements[6] = current_time.second

        #Create Filename
        filename = str(current_time)
        filename = filename.replace(' ', '-').split('.')[0]
        filename = filename.replace(':', '-')
        filename = '/home/pi/Code/psilocybin_greenhouse/data/lux/' + filename[:10] + '.csv'

        #Write
        with open(filename, 'a') as f:
            writestr = ''
            for j in range(7):
                if (j < 1):
                    writestr = writestr + str(measurements[j]) + ','
                else:
                    writestr = writestr + str(int(measurements[j])) + ','
            writestr = writestr[:-1] + '\n'
            print(writestr)
            f.write(writestr)

        #Sleep
        time.sleep(0.5)
