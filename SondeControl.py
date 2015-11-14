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

    def __init__(self, portIn = '/dev/ttyUSB0',  roboclawPort = '/dev/ttyACM0'):
        self.port = portIn
        self.virtualSonde = False
        self.lastDepth = 0
        
        try:
            roboclaw.Open(roboclawPort,115200)
        except:
            print "Couldn't open roboclaw on port ",  roboclawPort
            exit()
        
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
        if self.virtualSonde:
            return -1
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
        if self.virtualSonde:
            return '1,2,3'
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
        if self.virtualSonde:
            return '-1,1,2,3'
        timeStamp = self.readTime()
        #remove newline
        timeStamp = timeStamp.rstrip()
        data = self.readData()
        data = data.replace(" ",",")
       
        #chop off the last comma
        data = data[:-3]

        return timeStamp + "," + data + "\n"


    def getCurrentDepth(self):
        # buffer requests with small wait time to avoid flooding roboclaw
        time.sleep(.01)
        try:
            encoderCount = roboclaw.ReadEncM1(0x80)[0]
            self.lastDepth = encoderCount/-8200.0 * .06 * math.pi              

        except:
            print "ERROR in reading encoders"
            roboclaw.DutyAccelM1(0x80, 1500,0)

        return self.lastDepth


    def goToDepth(self,depth):
        # determine which way the winch should go
        sign = cmp(self.getCurrentDepth() - depth,0)
        start = time.time()

        # safety feature to prevent winch from over extending
        maxTime = abs(depth - self.lastDepth) / .2 * 11

        currentDepth = self.getCurrentDepth()
        # continue until the depth is passed by a little
        while sign * -1 != cmp(currentDepth - depth,0):
            currentDepth = self.getCurrentDepth()
            time.sleep(.1)
            roboclaw.DutyAccelM1(0x80, 1500,sign*-1*300)
            print "Current Depth: ", currentDepth, " Desired Depth: ", depth

            # stop out of control winch
            if time.time() - start > maxTime:
                break

        # stop the roboclaw
        print "Stopping roboclaw"
        # send multiple stop commands to ensure that one is received
        start = time.time()
        while time.time() - start < .5:
            roboclaw.DutyAccelM1(0x80, 1500,0)
            time.sleep(.1)

        self.lastDepth = depth
