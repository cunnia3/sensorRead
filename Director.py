# Author: Andrew Cunningham
# Email: andrew64ce@gmail.com
# Description:  This module serves as a director for operation of the sonde
#               system.  It contains an object that houses a command interface
#               in the form of a series of functions that are associated with text


import time
import sys
from SondeControl import SondeController
from DataManager import FileManager


# Director requires access to the SondeController and FileManager classes
# Director accesses the resources (SondeController and FileManager) and coordinates
# Their usage through a series of commands that are indexed by an associated string
class Director:
    'Contains a series of commands that can be called through a file or interactively'
    def __init__(self, commandFileName=""):
        self.mySonde = SondeController()
        self.myFileManager = FileManager()
  
        # build string to function dictionary
        self.commandDict = {'measurement_file':self.measurement_file_command,        
                            'log_file':self.log_file_command,
                            'goto_depth':self.goto_depth_command,
                            'record_measurements':self.record_measurements_command,
                            'wait':self.wait_command,
                            'end_profile':self.end_profile_command}
    
    ################
    # COMMAND LIST #
    ################

    def measurement_file_command(self, fileName):
        print "dummy change record file to " + fileName

    def log_file_command(self, fileName):
        print "dummy change log file to " + fileName

    def goto_depth_command(self, depth):
        self.mySonde.goToDepth(depth)

    def record_measurements_command(self):
        data = self.mySonde.getData()
        self.myFileManager.log(data)

    def wait_command(self, secondsToWait):
        time.sleep(secondsToWait)        

    def end_profile_command(self):
        print "dummy stopping profile"

    # function accepts a command array and then executes it
    def run_command(self, command):
        print "run dummy " + command

#myDirector = Director("commands.txt")

#How to call commands from a dictionary
#myDirector.commandDict['readCommands']()




# if there is a command line argument, it is a file to read with commands in it
if len(sys.argv) > 1:
    print "dummy file loaded " + argv[1]



# else there is no command file and work interactively
else:
    input = ""
    while input != 'q':
        print "$:",
        input = raw_input()
