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
                            'start_profile':self.start_profile,
                            'end_profile':self.end_profile_command}
    
    ################
    # COMMAND LIST #
    ################
    # Treat arguments to commands as an array that may only have 1 element

    def measurement_file_command(self, fileName):
        self.myFileManager.setRecordFile(fileName[0])

    def log_file_command(self, fileName):
        self.myFileManager.setLogFile(fileName[0])

    def goto_depth_command(self, depth):
        self.mySonde.goToDepth(float(depth[0]))
        self.myFileManager.log("Accepted goto_depth command going to depth " + depth[0])

    def record_measurements_command(self):
        data = self.mySonde.getData()
        self.myFileManager.record_measurements(data)
        self.myFileManager.log("Accepted record_measurements command")

    def wait_command(self, secondsToWait):
        time.sleep(int(secondsToWait[0]))
        self.myFileManager.log("Accepted wait command, waiting for " + secondsToWait[0])        

    def start_profile(self):
        self.myFileManager.getReadyToWrite()    

    def end_profile_command(self):
        exit()

    # function accepts a command array and then executes it
    def run_command(self, commandRaw):
        commandArray = commandRaw.split()
        command = commandArray.pop(0)
        arguments = commandArray
        # if no arguments to command
        if len(arguments) == 0:
#            try:
             self.commandDict[command]()         
#            except:
#                 print "unable to execute command " + command        
        # if arguments to command
        else:
            try:
                self.commandDict[command](arguments)
            except:
                print "unable to execute command " + command + " with arguments ",  arguments

#How to call commands from a dictionary
#myDirector.commandDict['readCommands']()


myDirector = Director("commands.txt")

# if there is a command line argument, it is a file to read with commands in it
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        commandLines = f.readlines()

    for commandLine in commandLines:
        myDirector.run_command(commandLine)

# else there is no command file and work interactively
else:
    input = ""
    while 1==1:
        print "$:",
        input = raw_input()
        if input == 'q' or input == 'exit' or input == 'quit':
            break
        myDirector.run_command(input)
