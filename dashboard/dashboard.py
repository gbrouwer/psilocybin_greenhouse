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

        #Find all the camera1 files locally
        local_camera1_files = []
        local_camera1_names = []
        for root, dirs, files in os.walk("../data/camera1", topdown=False):
            for name in files:
                if '.png' in name:
                    local_camera1_files.append(os.path.join(root, name))
                    local_camera1_names.append(name)

        #Find all the camera2 files locally
        local_camera2_files = []
        local_camera2_names = []
        for root, dirs, files in os.walk("../data/camera2", topdown=False):
            for name in files:
                if '.png' in name:
                    local_camera2_files.append(os.path.join(root, name))
                    local_camera2_names.append(name)

        #Create Files for what is on Greenhouse
        os.system('ssh pi@greenhouse ls -l /home/pi/Code/psilocybin_greenhouse/data/measurements/ > measurements.out')
        os.system('ssh pi@greenhouse ls -l /home/pi/Code/psilocybin_greenhouse/data/camera1/ > camera1.out')
        os.system('ssh pi@greenhouse ls -l /home/pi/Code/psilocybin_greenhouse/data/camera2/ > camera2.out')
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

        #Open each remote filelist and create a remote list
        remote_camera1_names = []
        remote_camera1_files = []
        with open('camera1.out','r') as f:
            f.readline()
            for line in f:
                remote_camera1_name = line.rstrip().split(' ')[-1]
                remote_camera1_file = 'home/pi/Code/psilocybin_greenhouse/data/camera1/' + remote_camera1_name
                remote_camera1_names.append(remote_camera1_name)
                remote_camera1_files.append(remote_camera1_file)

        #Open each remote filelist and create a remote list
        remote_camera2_names = []
        remote_camera2_files = []
        with open('camera2.out','r') as f:
            f.readline()
            for line in f:
                remote_camera2_name = line.rstrip().split(' ')[-1]
                remote_camera2_file = 'home/pi/Code/psilocybin_greenhouse/data/camera2/' + remote_camera2_name
                remote_camera2_names.append(remote_camera2_name)
                remote_camera2_files.append(remote_camera2_file)

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

        # #See Which ones to copy
        local_camera1_names = np.sort(local_camera1_names).tolist()
        local_camera1_files = np.sort(local_camera1_files).tolist()
        remote_camera1_names = np.sort(remote_camera1_names).tolist()
        for r,remote_camera1_name in enumerate(remote_camera1_names):
            if (remote_camera1_name not in local_camera1_names):
                cmd = 'scp pi@greenhouse:/' + remote_camera1_files[r] + ' ../data/camera1/' + remote_camera1_names[r]
                os.system(cmd)

        # #See Which ones to copy
        local_camera2_names = np.sort(local_camera2_names).tolist()
        local_camera2_files = np.sort(local_camera2_files).tolist()
        remote_camera2_names = np.sort(remote_camera2_names).tolist()
        for r,remote_camera2_name in enumerate(remote_camera2_names):
            if (remote_camera2_name not in local_camera2_names):
                cmd = 'scp pi@greenhouse:/' + remote_camera2_files[r] + ' ../data/camera2/' + remote_camera2_names[r]
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

        #Create Dashboard
        dashboard_image = np.zeros((480+300,90+(640*2),3)).astype('uint8')
        dashboard_image[:] = 128
        image1_file = '../data/camera1/' + remote_camera1_names[-2]
        image2_file = '../data/camera2/' + remote_camera2_names[-2]

        try:
            image1 = cv2.imread(image1_file)
            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
            image2 = cv2.imread(image2_file)
            image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

            dashboard_image[30:480+30,700:-30,:] = image2
            dashboard_image[30:480+30,30:670,:] = image1
            dashboard_image = dashboard_image.astype('uint8')
            window_name = 'image'
        except:
            print('corrupt image')

        #Add Current Humidity and Temperature
        text1 = "Current Temperature: " + str(measurement_data[-1,0])
        text2 = "Current Light Level: " + str(lux_data[-1,0])
        text3 = "Current Humidity: " + str(measurement_data[-1,1])
        font = cv2.FONT_HERSHEY_SIMPLEX
        org1 = (30, 600)
        org2 = (30, 650)
        org3 = (30, 700)
        fontScale = 1
        color = (255, 255, 255)
        thickness = 2
        dashboard_image = cv2.putText(dashboard_image, text1, org1, font, fontScale, color, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text2, org2, font, fontScale, color, thickness, cv2.LINE_AA, False)
        dashboard_image = cv2.putText(dashboard_image, text3, org3, font, fontScale, color, thickness, cv2.LINE_AA, False)

        #Show
        cv2.imshow(window_name, dashboard_image)

        #Wait
        cv2.waitKey(1000)
