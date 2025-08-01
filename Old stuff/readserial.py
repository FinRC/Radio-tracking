#!/usr/bin/python

import datetime
import time
import serial

# Set up serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

#Examples of serial data:
#
#Location message:
#$PKNSH,6010.3193,N,02443.7783,E,094600,A,000000101,*0A
#123456789012345678901234567890123456789012345678901234
#         111111111122222222223333333333444444444455555
#
#Message type=1:6
#LAT=8:17
#LON=20:30
#Unit ID=44:51
#
#Status message:
#xE0000001010000009990002
#123456789012345678901234
#         111111111122222
#
#Message type=1:4
#Sending Unit ID=5:12
#Destination Unit ID=14:21
#Status code=23:25

def main(): 

	while True:
		line=ser.readline()
		print(line)

main()

ser.close()
