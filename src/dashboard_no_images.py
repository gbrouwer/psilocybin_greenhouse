import os
import sys
import cv2
import pandas as pd
import numpy as np
import time
import imageio
from PIL import Image


#------------------------------------------------------
if __name__ == '__main__':

    while True:

        #Find all the measurement files locally
        local_measurement_files = []
        local_measurement_names = []
        for root, dirs, files in os.walk("../data/measurements", topdown=False):
            for name in files:
                if '.csv' in name:
                    local_measurement_files.append(os.path.join(root, name))
                    local_measurement_names.append(name)

        #Find all the measurement files locally
        local_lux_files = []
        local_lux_names = []
        for root, dirs, files in os.walk("../data/lux", topdown=False):
            for name in files:
                if '.csv' in name:
                    local_lux_files.append(os.path.join(root, name))
                    local_lux_names.append(name)

        #Create Files for what is on Greenhouse
        os.system('ssh pi@greenhouse ls -l /home/pi/Code/psilocybin_greenhouse/data/measurements/ > measurements.out')
        os.system('ssh pi@greenhouse ls -l /home/pi/Code/psilocybin_greenhouse/data/lux/ > lux.out')

        #Open each remote filelist and create a remote list
        remote_measurement_names = []
        remote_measurement_files = []
        with open('measurements.out','r') as f:
            f.readline()
            for line in f:
                remote_measurement_name = line.rstrip().split(' ')[-1]
                remote_measurement_file = 'home/pi/Code/psilocybin_greenhouse/data/measurements/' + remote_measurement_name
                remote_measurement_names.append(remote_measurement_name)
                remote_measurement_files.append(remote_measurement_file)

        #Open each remote filelist and create a remote list
        remote_lux_names = []
        remote_lux_files = []
        with open('lux.out','r') as f:
            f.readline()
            for line in f:
                remote_lux_name = line.rstrip().split(' ')[-1]
                remote_lux_file = 'home/pi/Code/psilocybin_greenhouse/data/lux/' + remote_lux_name
                remote_lux_names.append(remote_lux_name)
                remote_lux_files.append(remote_lux_file)

        # #See Which ones to copy
        local_measurement_names = np.sort(local_measurement_names).tolist()
        local_measurement_files = np.sort(local_measurement_files).tolist()
        remote_measurement_names = np.sort(remote_measurement_names).tolist()
        remote_measurement_files = np.sort(remote_measurement_files).tolist()
        for r,remote_measurement_name in enumerate(remote_measurement_names):
            if (remote_measurement_name not in local_measurement_names):
                cmd = 'scp pi@greenhouse:/' + remote_measurement_files[r] + ' ../data/measurements/' + remote_measurement_names[r]
                os.system(cmd)

        #Make Sure to overwrite the last measurement file because it will have been updated
        cmd = 'scp pi@greenhouse:/' + remote_measurement_files[-1] + ' ../data/measurements/' + remote_measurement_names[-1]
        os.system(cmd)

        # #See Which ones to copy
        local_lux_names = np.sort(local_lux_names).tolist()
        local_lux_files = np.sort(local_lux_files).tolist()
        remote_lux_names = np.sort(remote_lux_names).tolist()
        remote_lux_files = np.sort(remote_lux_files).tolist()
        for r,remote_lux_name in enumerate(remote_lux_names):
            if (remote_lux_name not in local_lux_names):
                cmd = 'scp pi@greenhouse:/' + remote_lux_files[r] + ' ../data/lux/' + remote_lux_names[r]
                os.system(cmd)

        #Make Sure to overwrite the last measurement file because it will have been updated
        cmd = 'scp pi@greenhouse:/' + remote_lux_files[-1] + ' ../data/lux/' + remote_lux_names[-1]
        os.system(cmd)

        #Open Measurement File
        measurements = pd.read_csv('../data/measurements/' + remote_measurement_names[-1],header=None)
        columns = ['pressure','height','pressureTemperature','humidity','humidityTemperature']
        columns = columns + ['year','month','day','hour','minute','second']
        measurements.columns = columns
        measurement_data = measurements[['pressureTemperature','humidity']].values

        #Open Lux File
        lux = pd.read_csv('../data/lux/' + remote_measurement_names[-1],header=None)
        columns = ['lux']
        columns = columns + ['year','month','day','hour','minute','second']
        lux.columns = columns
        lux_data = lux[['lux']].values

        #dashboard_image = np.zeros((480,640,3)).astype('uint8')
        dashboard_image = cv2.imread('../assets/images/background2.png')

        #Add Current Humidity and Temperature
        text1 = "Current Temperature: " + str(np.round(measurement_data[-1,0],2))
        text2 = "Current Light Level: " + str(np.round(lux_data[-1,0],2))
        text3 = "Current Humidity: " + str(np.round(measurement_data[-1,1],2))
        font = cv2.FONT_HERSHEY_SIMPLEX
        org1 = (30, 80)
        org2 = (30, 130)
        org3 = (30, 180)
        org4 = (31, 81)
        org5 = (31, 131)
        org6 = (31, 181)
        fontScale = 0.75
        color = (255, 255, 255)
        black = (0,0,0)
        thickness = 2
        dashboard_image = cv2.putText(dashboard_image, text1, org4, font, fontScale, black, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text2, org5, font, fontScale, black, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text3, org6, font, fontScale, black, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text1, org1, font, fontScale, color, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text2, org2, font, fontScale, color, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text3, org3, font, fontScale, color, thickness, cv2.LINE_AA, False)

        #Show
        window_name = 'test'
        # cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, dashboard_image)

        #Wait
        cv2.waitKey(1000)

        # except:
        #     print('corrupt image')
