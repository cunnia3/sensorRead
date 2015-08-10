# Author: Andrew Cunningham
# Email: andrew64ce@gmail.com
# Description:  This module serves as a director for operation of the sonde
#               system.  It contains an object that will read a command
#               script and then execute the commands


import SondeControl

class Director:
    'Extracts commands from command files and then executes them'
    def __init__(self, commandFileName):
        #self.mySonde = SondeReader('/dev/ttyUSB0')
        # open command file
        try:
            self.commandFile = open(commandFileName)
        except:
            print "File open error"
            exit()
    
    # read commands from the file and return an array of them, store them in     
    def readCommands():
        


