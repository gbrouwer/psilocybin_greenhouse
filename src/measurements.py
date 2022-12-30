import sys, getopt
import cv2
import numpy as np
import imageio
from datetime import datetime
from sense_hat import SenseHat
sys.path.append('.')
import RTIMU
import os.path
import numpy as np
import time
import math
from datetime import datetime
SETTINGS_FILE = "RTIMULib"

#Compute Height
def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));

#Main
if __name__ == '__main__':

    # Parameters
    black = (0, 0, 0)
    white = (128, 250, 250)
    sense = SenseHat()
    sense.clear(black)
    sense.set_rotation(180)

    #Information
    # #print("Using settings file " + SETTINGS_FILE + ".ini")
    # if not os.path.exists(SETTINGS_FILE + ".ini"):
    #     print("Settings file does not exist, will be created")

    #Measure
    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)
    pressure = RTIMU.RTPressure(s)
    humidity = RTIMU.RTHumidity(s)

    #More Information
    print("IMU Name: " + imu.IMUName())
    print("Pressure Name: " + pressure.pressureName())
    print("Humidity Name: " + humidity.humidityName())

    #Failure
    if (not imu.IMUInit()):
        print("IMU Init Failed")
        sys.exit(1)
    else:
        print("IMU Init Succeeded");

    #Turn on sensors
    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    #Failure to start sensors
    if (not pressure.pressureInit()):
        print("Pressure sensor Init Failed")
    else:
        print("Pressure sensor Init Succeeded")
    if (not humidity.humidityInit()):
        print("Humidity sensor Init Failed")
    else:
        print("Humidity sensor Init Succeeded")

    #Get Best Polling Interval
    poll_interval = imu.IMUGetPollInterval()
    print("Recommended Poll Interval: %dmS\n" % poll_interval)

    while True:
        if imu.IMURead():
            current_time = datetime.now()
            filename = str(current_time)
            filename = filename.replace(' ', '-').split('.')[0]
            filename = filename.replace(':', '-')
            filename = '/home/pi/Code/psilocybin_greenhouse/data/measurements/' + filename[:10] + '.csv'
            with open(filename, 'a') as f:
                measurements = np.zeros((11))
                measurements[5] = current_time.year
                measurements[6] = current_time.month
                measurements[7] = current_time.day
                measurements[8] = current_time.hour
                measurements[9] = current_time.minute
                measurements[10] = current_time.second
                data = imu.getIMUData()
                (data["pressureValid"], data["pressure"], data["pressureTemperatureValid"], data["pressureTemperature"]) = pressure.pressureRead()
                (data["humidityValid"], data["humidity"], data["humidityTemperatureValid"], data["humidityTemperature"]) = humidity.humidityRead()
                fusionPose = data["fusionPose"]
                #print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
                if (data["pressureValid"]):
                    measurements[0] = data["pressure"]
                    measurements[1] = computeHeight(data["pressure"])
                    print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["pressure"])))
                if (data["pressureTemperatureValid"]):
                    print("Pressure temperature: %f" % (data["pressureTemperature"]))
                    measurements[2] = data["pressureTemperature"]
                if (data["humidityValid"]):
                    print("Humidity: %f" % (data["humidity"]))
                    measurements[3] = data["humidity"]
                if (data["humidityTemperatureValid"]):
                    print("Humidity temperature: %f" % (data["humidityTemperature"]))
                    measurements[4] = data["humidityTemperature"]

                #Write
                writestr = ''
                for j in range(11):
                    if (j < 5):
                        writestr = writestr + str(measurements[j]) + ','
                    else:
                        writestr = writestr + str(int(measurements[j])) + ','
                writestr = writestr[:-1] + '\n'
                print(writestr)
                f.write(writestr)
                time.sleep(poll_interval*1.0/10.0)

