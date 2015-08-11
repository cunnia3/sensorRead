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
class SondeController:
    'Sonde System communication handler'

    def __init__(self):
        print "dummy initialized Sonde"

    def getData(self):
        print "dummy line from getCSVLine"

    def goToDepth(self, desiredDepth):
        print "dummy set depth to: " + desiredDepth
        time.sleep(2)
        print "done setting dummy depth"
