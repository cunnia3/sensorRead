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
import roboclaw
import math

# This class handles all of the communication with
# the sonde sensor

class SondeController:
    'Sonde communication handler'

    def __init__(self, portIn = '/dev/ttyUSB0'):
        self.port = portIn
        self.virtualSonde = False
        self.lastDepth = 0
        
        # initialize the serial communication
        try:
            self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)
        except:
            print "No sonde detected, using virtual sonde"
            self.virtualSonde = True       



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


    def getData(self):
        timeStamp = self.readTime()
        #remove newline
        timeStamp = timeStamp.rstrip()
        data = self.readData()
        data = data.replace(" ",",")
       
        #chop off the last comma
        data = data[:-3]

        return timeStamp + "," + data + "\n"


    def getCurrentDepth(self):
        try:
            encoderCount = roboclaw.readM2encoder()[0]
            self.lastDepth = encoderCount/-8200.0 * .06 * math.pi              

        except:
            print "ERROR in reading encoders"
            roboclaw.SetM2DutyAccel(1500,0)

        return self.lastDepth


    def goToDepth(self,depth):
        # determine which way the winch should go
        sign = cmp(self.getCurrentDepth() - depth,0)
        # continue until the depth is passed by a little
        while sign * -1 != cmp(self.getCurrentDepth() - depth,0):
            roboclaw.SetM2DutyAccel(1500,sign*-1*300)
            print "Current Depth: ", self.getCurrentDepth(), " Desired Depth: ", depth
            time.sleep(.1)

        # stop the roboclaw
        roboclaw.SetM2DutyAccel(1500,0)


