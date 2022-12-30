import os
import sys
import subprocess
import pathlib
import json
from utils import find_base_dir
from listener import Listener

#------------------------------------------------
if __name__ == '__main__':

    os.system('sudo killall VDCAssistant')
    os.system('sudo sysctl -w net.inet.udp.maxdgram=65536')

    #Reset all python ports using 3000
    cmd = 'lsof -i:3000 > ../data/messages/proc_3000'
    os.system(cmd)

    #Open file and read
    pids = []
    with open('../data/messages/proc_3000','r') as f:
        for line in f:
            elements = line.rstrip().split(' ')
            pid = elements[2]
            pids.append(pid)

    #Kill
    for pid in pids:
        if (len(pid) > 0):
            cmd = 'kill -9 ' + pid
            print(cmd)
            os.system(cmd)

    #Reset all python ports using 6666
    cmd = 'lsof -i:6666 > ../data/messages/proc_6666'
    os.system(cmd)

    #Open file and read
    pids = []
    with open('../data/messages/proc_6666','r') as f:
        for line in f:
            elements = line.rstrip().split(' ')
            if (elements[0] == 'Python'):
                pid = elements[2]
                pids.append(pid)

    #Kill
    for pid in pids:
        if (len(pid) > 0):
            cmd = 'kill -9 ' + pid
            print(cmd)
            os.system(cmd)

    #Kill all active processes
    os.system('pm2 delete all')

    #Start Node
    os.system('pm2 start ../node/websocket.mjs')

    #Get Hostname
    basedir = find_base_dir()
    result = subprocess.run(['hostname'], stdout=subprocess.PIPE)
    hostname = str(result.stdout)[2:-3]
    with open(basedir + '/.settings/hosts.json') as f:
        hosts = json.load(f)
    host = hosts[hostname]
    processes = host['processes']
    print(processes)

    # #Start Camera
    # if 'camera' in module_roles:
    #     os.system('pm2 start camera.py --name camera --interpreter=python3')

    # Start Vision
    if 'vision' in processes:
        os.system('pm2 start vision.py --name vision --interpreter=python3')

    # # Start Microphone
    # if 'microphone' in module_roles:
    #     os.system('pm2 start microphone.py --name microphone --interpreter=python3')
    #
    # # Start Audio
    # if 'audio' in module_roles:
    #     os.system('pm2 start audio.py --name audio --interpreter=python3')


    # Start Unity
    if 'unity' in processes:
        os.system('../bin/samson-unity.app/Contents/MacOS/samson-unity &')