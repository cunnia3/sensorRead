import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

ser.write('\r')
print ser.write('time\r')
test1 = ser.readline()
test2 = ser.readline()
test3 = ser.readline()
print test1
print test2
print test3


