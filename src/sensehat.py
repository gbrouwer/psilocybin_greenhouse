import os
import sys
import numpy as np
import time
import json
import wave
import pickle

import threading
import pyaudio
import simpleaudio as sa
import pathlib
# import seaborn as sns

import pathlib
import requests
import websocket
import _thread
import subprocess

from sense_hat import SenseHat
from time import sleep
from random import randint
from utils import get_hostname
from utils import find_base_dir
from datetime import datetime
from websocket import create_connection
from websocket_wrapper import websocketWrapper
# from speech_detection_module import SpeechDetectionModule

# ---------------------------------------------------------------------------
class SensingHat:

    # Init
    def __init__(self,):
        # self.basedir = find_base_dir()
        # self.settings = ''
        self.name = ''
        self.hostname = ''
        # self.sense = SenseHat()
        # self.websockets = {}
        # self.receive_threads = {}
        # self.configure()
        # self.current_stream = 'strawberry'
        # self.speechModule = SpeechDetectionModule()
        # self.process_frames = []
        # self.form_1 = pyaudio.paInt16
        # self.chans = 1
        # self.samp_rate = 16000
        # self.chunk = 2000
        # self.record_secs = 1.0
        # self.dev_index = 2
        # self.audio = pyaudio.PyAudio()

    # def configure(self):
    #     result = subprocess.run(['hostname'], stdout=subprocess.PIPE)
    #     self.hostname = str(result.stdout)[2:-3]
    #     with open(self.basedir + '/.settings/hosts.json') as f:
    #         hosts = json.load(f)
    #     self.settings = hosts[self.hostname]
    #     self.name = self.settings['name']
    #     self.websockets_info = self.settings['websockets']
    #     self.socket_name = self.settings['socket_name']
    #     self.socket_port = self.settings['socket_port']
    #     self.vision_websocket = self.settings['vision_websocket']
    #
    # def connect(self,name):
    #
    #     # Create Sockets
    #     for item in self.websockets_info:
    #         self.websockets[item['name']] = websocketWrapper(name,item['name'],item['ip'], item['port'])
    #         self.websockets[item['name']].open()
    #         self.websockets[item['name']].register()
    #
    # def start_receive_threads(self):
    #
    #     # Create Receive Threads
    #     for item in self.websockets:
    #         listener = Listener(self.websockets[item])
    #         self.updates.append(listener.timestamp)
    #         self.listeners.append(listener)
    #
    #     self.receiver = threading.Thread(target=self.receive)
    #     self.receiver.start()
    #
    # def receive(self):
    #
    #     #Receiver
    #     while True:
    #         for index,listener in enumerate(self.listeners):
    #             if (self.updates[index] != listener.timestamp):
    #                 self.updates[index] = listener.timestamp
    #                 if ('data' in listener.recv_object):
    #                     data = listener.recv_object['data']
    #                     if (data['type'] == 'command'):
    #                         self.execute_commands(data)
    #                     if (data['type'] == 'data'):
    #                         if (self.current_stream == 'blackberry'):
    #                             self.process_data(data)
    #
    # @staticmethod
    # def execute_commands(data):
    #
    #     # Execute Commands
    #     for cmd in data['commands']:
    #         exec(cmd)
    #
    # def detection(self):
    #
    #     while True:
    #         time.sleep(1.0)
    #         self.senddata = {}
    #         if (len(self.process_frames) == 8):
    #             self.speechModule.classify(self.process_frames)
    #             self.senddata = self.speechModule.senddata
    #             self.senddata['type'] = 'data'
    #             self.senddata['modality'] = 'speech'
    #             self.websockets['strawberry'].send(['strawberry_core_strawberry'], self.senddata,'peer2peer')
    #
    #
    # def microphone_loop(self):
    #
    #     #Create pyaudio stream
    #     stream = self.audio.open(format = self.form_1,rate = self.samp_rate,channels = self.chans,
    #                         input_device_index = self.dev_index,input = True,
    #                         frames_per_buffer=self.chunk)
    #
    #     #Loop Indefinitely
    #     while True:
    #         data = []
    #         frames = []
    #         for ii in range(0, int((self.samp_rate / self.chunk) *self. record_secs)):
    #             try:
    #                 data = stream.read(self.chunk)
    #                 frames.append(data)
    #                 if (len(frames) > 8):
    #                     frames = frames[-8:]
    #                 if (len(frames) == 8):
    #                     self.process_frames = frames[:]
    #             except:
    #                 print('error')


# ------------------------------------------------------------
if __name__ == '__main__':

    # Init
    nodename = get_hostname()
    print('PID: ', os.getpid())
    print('Nodename:', nodename)

    # # Instantiate
    # sensingHat = SensingHat()

    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    sense = SenseHat()

    while True:
        sense.show_message("Astro Pi is awesome!", text_colour=yellow, back_colour=blue, scroll_speed=0.05)

    # # Connect to Websocket
    # microphone.id = microphone.name + '_camera'
    # microphone.connect(microphone.name + '_microphone')
    #
    # # Start Receive Threads
    # microphone.start_receive_threads()
    #
    # # Detection Process Threads
    # microphone.detection_thread = threading.Thread(target=microphone.detection)
    # microphone.detection_thread.start()
    #
    # # Start microphone loop
    # microphone.microphone_loop()