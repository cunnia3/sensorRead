import datetime
import time

class FileManager:
    'manages writing data to files and loggign error messages'
    def __init__(self):
        self.recordFileName = "test_record"
        self.recordFile = None
        self.logFileName = "test_log"    
        self.logFile = None
        self.readyToWrite = False

    def setRecordFile(self, fileName):
        self.recordFileName = fileName

    def setLogFile(self, fileName):
        self.logFileName = fileName

    def getReadyToWrite(self):
        self.logFile = open(self.logFileName, "w+")
        self.recordFile = open(self.recordFileName, "w+")
        self.readyToWrite = True

    def record_measurements(self, measurementString):
	if self.readyToWrite:
            self.recordFile.write(measurementString)

    def log(self, logMessage):
        if self.readyToWrite:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            self.logFile.write(st + " " + logMessage + "\n")
