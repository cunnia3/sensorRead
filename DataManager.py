class FileManager:
    'manages writing data to files and loggign error messages'
    def __init__(self):
        print "dummy file manager init"
        self.recordFile = ""
        self.logFile = ""    

    def record_measurements(self, measurementString):
        print "dummy recorded: " + measurementString

    def log(self, logMessage):
        print "dummy log: " + logMessage
