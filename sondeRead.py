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


class ReadManager:
    'Object responsible for scheduling reads from a Sonde and writing data'
    # frequency = readings per minute | duration = how long to record in minutes -1 would be forever
    def __init__(self, sonde, frequency = 5, file = os.popen("date +'%m_%d_%y'").readline().rstrip() + ".csv", duration = 1):
        self.frequency = frequency
        self.waitTime = 60.0/frequency
        self.file = file
        self.duration = duration
        self.sonde = sonde

    # record data to the specified file, runs in its own thread    
    def recordData(self):
        start_time = time.time()
        elapsed_time = time.time() - start_time
        writesSoFar = 0

        #open file
        file = open(self.file,"w+")

        while elapsed_time/60 < self.duration:
            nextWriteTime = writesSoFar * self.waitTime
            elapsed_time = time.time() - start_time
            # read and record at correct frequency
            if elapsed_time >= nextWriteTime:
                writesSoFar += 1
                csvEntry = self.sonde.getCSVLine()
                file.write(csvEntry)             

        print "Finished recording period"
        file.close()

    def udpQueryServer(self):
        # initialize port settings
        UDP_IP = "127.0.0.1"
        UDP_PORT = 4567
        
        receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver.bind((UDP_IP, UDP_PORT))

        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # wait for a message to be received through UDP
        # obtain requester's ip from the packet's address and the port
        # from the message's data
        while True:
            port, addr = receiver.recvfrom(1024)
            ip = addr[0]
            MESSAGE = self.sonde.getCSVLine()
            print "ip: ", addr[0], " port: ", port, " message: ", MESSAGE
            
            sender.sendto(MESSAGE, (ip, int(port)))


# TODO: auto port selection
mySonde = SondeReader('/dev/ttyUSB0')
myReader = ReadManager(mySonde)

try:
    # set up threads with daemons
    recordThread = threading.Thread(target=myReader.recordData)
    recordThread.daemon = True
    serverThread = threading.Thread(target=myReader.udpQueryServer)
    serverThread.daemon = True
    # start threads
    recordThread.start()
    serverThread.start()

except:
    print "Error: unable to start threads"

# keep main thread busy while worker threads work
while True:
    time.sleep(1)
