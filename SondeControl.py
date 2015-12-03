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
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
            return '-1,1,2,3\n'
        timeStamp = self.readTime()
        #remove newline
        timeStamp = timeStamp.rstrip()
        data = self.readData()
        data = data.replace(" ",",")
       
        #chop off the last comma
        data = data[:-3]

        return timeStamp + "," + data + "\n"


    # Read the mode switch to see which mode we are in FALSE = autonomous, TRUE = manual
    def inManualMode(self):
        return GPIO.input(18)


    def manualMode(self):
        # while we are in manual mode, accept button inputs to move winch
        while self.inManualMode():
            if GPIO.input(23):
                roboclaw.DutyAccelM1(0x80, 5000,15000)
            elif GPIO.input(25):
                roboclaw.DutyAccelM1(0x80, 5000,-15000)
            else:
                roboclaw.DutyAccelM1(0x80, 30000,0) 

        # reset encoders 
        roboclaw.ResetEncoders(0x80)
        roboclaw.DutyAccelM1(0x80, 30000,0)
        return
        


    def getCurrentDepth(self):
        # buffer requests with small wait time to avoid flooding roboclaw
        time.sleep(.01)
        try:
            encoderCount = roboclaw.ReadEncM1(0x80)[1]
            #print "encoderCount = ",  encoderCount
            # calculate depth in meters .9 is calibration
            self.lastDepth = encoderCount/-4000.0 * .15 * 1.1 *math.pi              

        except:
            print "ERROR in reading encoders"
            roboclaw.DutyAccelM1(0x80, 1500,0)

        return self.lastDepth


    def goToDepth(self,depth):
        # determine which way the winch should go
        sign = cmp(self.getCurrentDepth() - depth,0)
        start = time.time()

        # safety feature to prevent winch from over extending
        maxTime = abs(depth - self.lastDepth) / .2 * 25

        currentDepth = self.getCurrentDepth()
        # continue until the depth is passed by a little
        while sign * -1 != cmp(currentDepth - depth,0):

            # check to see if we are in manual mode before proceeding
            if self.inManualMode():
                roboclaw.DutyAccelM1(0x80, 30000,0)
                return

            currentDepth = self.getCurrentDepth()
            time.sleep(.1)
            roboclaw.DutyAccelM1(0x80, 4000,sign*-1*18000)
            print "Current Depth: ", currentDepth, " Desired Depth: ", depth

            # stop out of control winch
            if time.time() - start > maxTime:
                break

        # stop the roboclaw
        #print "Stopping roboclaw"
        # send multiple stop commands to ensure that one is received
        start = time.time()
        while time.time() - start < .5:
            roboclaw.DutyAccelM1(0x80, 10000,0)
            time.sleep(.1)

        self.lastDepth = depth
