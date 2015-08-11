class FileManager:
    'manages writing data to files and loggign error messages'
    def __init__(self):
        print "dummy file manager init"
        self.recordFile = "test_record"
        self.logFile = "test_log"    

    def setRecordFile(self, fileName):
        self.recordFile = fileName

    def setLogFile(self, fileName):
        self.logFile = fileName

    def record_measurements(self, measurementString):
        f = open(self.recordFile,"w+")
        f.write(measurementString)
        f.close()
        self.log("Recorded measurement string")

    def log(self, logMessage):
        f = open(self.logFile,"w+")
        f.write(logMessage)
        f.close()
