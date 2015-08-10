# Author: Andrew Cunningham
# Email: andrew64ce@gmail.com
# Description: This program regularly collects information
#              from the sonde sensor over the RS232 serial
#              communication line at a specified frequency
#              and saves the results into a csv file in one
#              thread and hosts a UDP query server which 
#              serves live sensor readings in another thread

import serial
import os
import time
import threading
import socket

# This class handles all of the communication with
# the sonde sensor
class SondeReader:
    'Sonde communication handler'

    def __init__(self, portIn):
        self.port = portIn
        self.lock = threading.RLock()
        
        # initialize the serial communication
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)
       

    def readTime(self):
        #flush any bad previous input        
        self.ser.write('\r')
        self.ser.write('time\r')

        # read three lines of serial output because the
        # sonde provides output for terminal interfacing
        time = None 
        for x in range(0, 3):
            time = self.ser.readline()
           
        return time


    def readData(self):
        # flush any bad previous input
        self.ser.write('\r')
        self.ser.write('data\r')

        # read three lines of serial output because the
        # sonde provides output for terminal interfacing
        data = None 
        for x in range(0, 3):
            data = self.ser.readline()
           
        return data


    def getCSVLine(self):
        self.lock.acquire()
        try:
            timeStamp = self.readTime()
            #remove newline
            timeStamp = timeStamp.rstrip()
            data = self.readData()
            data = data.replace(" ",",")
       
            #chop off the last comma
            data = data[:-3]

        finally:
            self.lock.release()
        return timeStamp + "," + data + "\n"



