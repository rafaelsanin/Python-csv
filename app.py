from serial import Serial
from threading import Thread
from Queue import Queue
import signal
import sys
import json
import csv
import requests

TOKEN = "BBFF-rVbMBsJtRQsOs1l0JFO9PITFpUEKW4"  # Put your TOKEN here
DEVICE_LABEL = "arduino"  # Put your device label here
VARIABLE_LABEL_1 = "current"  # Put your first variable label here
VARIABLE_LABEL_2 = "voltage"  # Put your second variable label here
VARIABLE_LABEL_3 = "temperature"  # Put your second variable label here

class serialWatcher (Thread, Serial):
    def __init__(self, q, port = 'COM15', baudrate = 115200):
        Thread.__init__(self)
        Serial.__init__(self, port, baudrate)
        self.daemon = True
        self.queue = q
    def run(self):
        self.running = True
        while self.running:
            if self.in_waiting:
                line = self.readline()[0:-1];
                try:
                    data = json.loads(line)
                    self.queue.put(data)
                    # print "Sensor data in Queue"
                except:
                    # print "Invalid data discarted"
                    pass
    def stop(self):
        self.running = False

data_queue = Queue(10)
sensor = serialWatcher(q = data_queue)
sensor.start()

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def data_process(data):
    print "Dato siendo procesado...\n"
    print data

def datalogging(data):
    f = csv.writer(open("test.csv", "w+"))

    array=[0,0,0]
    i=0
    for key,value in data.items():
        print value
        array[i]=value
        i+=1

    f.writerow(array)

while True:
    if not data_queue.empty():
        data = data_queue.get()
        data_process(data)
        datalogging(data)
