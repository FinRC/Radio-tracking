#!/usr/bin/python

# Kenwood NEXEDGE radio tracker for status and position reporting
#
# This code reads serial data from connected Kenwood NEXEDGE radio with COM port configured as 'Data + GPS data output'.
# Data is processed to output status codes & position to logfile and send position data as HTTP GET to a mapping portal
#
# This is My First Python program ever so apologies for bad syntaxes, confusing usage of functions etc.
# You may improve this if you want, just send me the updated version :)
#
# Erik Finskas OH2LAK <erik.finskas@gmail.com>

version = '17.8.2017-01'

import datetime
import time
import serial
import logging
import requests

# Set up logging
logger = logging.getLogger('GPS')
hdlr = logging.FileHandler('/var/log/NEXEDGE_tracker.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

# Set up serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

logger.info('***********')
logger.info('Kenwood NEXEDGE radio tracker version %s started' %version)
#print('Serial port %s opened' %ser)
logger.info('Serial port %s opened' %ser)

#Examples of serial data:
#
#Location message:
#$PKLSH,6100.5898,N,02527.6523,E,111500,A,100,1103,*27
#$PKNSH,6100.5899,N,02527.6527,E,103900,A,U00103,*56
#123456789012345678901234567890123456789012345678901
#         111111111122222222223333333333444444444455
#
#Message type=1:6
#LAT=8:17
#LON=20:30
#Unit ID=45:48
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

# Map unit ID's to Unit names
Unit_Aliases= {
    '101' : 'Team A',
    '102' : 'Team B',
    '103' : 'Team C',
    '104' : 'Team D',
    '105' : 'Team E',
    '106' : 'Team F',
    '107' : 'Team 7',
    '108' : 'Team 8',
    '109' : 'Team 9',
}

def main(): 

	while True:
		datenow = datetime.date.today()
		timenow = time.strftime('%H:%M:%S')
		line=ser.readline()
		MsgHeader=line[1:7]

		if MsgHeader == '$PKNSH':
			MsgProto='NXDN'
			#NXDN data message with $PKNSH header
			#print "Message type is NXDN location data"
			#print(line)	
			# GPSLat & GPSLon delivers position degrees, GPSHem and GPSMer provide hemisphere and side of meridian info 
			GPSLat = line[8:17]
       			GPSLon = line[20:30]
			GPSHem = line[18:19]
			GPSMer = line[31:32]
			# Add hemisphere and meridian designation respectively in middle of position coordinates after degrees
			Lat = GPSLat[:2] + GPSHem + GPSLat[2:]
			Lon = GPSLon[:3] + GPSMer + GPSLon[3:]		
       			UnitID=line[45:48]
			# Find UnitAlias from the dictionary referred by the UnitID number
                        UnitAlias=Unit_Aliases.get(UnitID)
                        output=('Unit %s (%s) reported position %s %s via %s' % (UnitID, UnitAlias, Lat, Lon, MsgProto))
                        #logger.info('Raw message: ' + str(line)) 
			logger.info(output)
			#print(output)
                        # Format the HTTP GET URL with variables
                        httpget = ('http://havu.hylly.org/api/msg?msg=$POS|WGS84|%s|%s|%s|%s|%s|0|0*' % (UnitAlias, datenow, timenow, Lat, Lon))
                        #print(httpget)
                        httprequest = requests.get(httpget)
                        if httprequest.status_code == 200:
                                SCOMS_status = ('SCOMS: ' + UnitAlias + ' position updated successfully')
                        else:
                                SCOMS_status = ('SCOMS: ' + UnitAlias + ' position update error. HTTP code ' + str(httprequest.status_code))
                        logger.info(SCOMS_status)
                        #print httprequest.status_code
                        #print httprequest.headers
                        #print httprequest.content


		elif MsgHeader == '$PKLSH':
			MsgProto='FleetSync'
			#FleetSync messages with $PKLSH header
			print "Message type is FleetSync location data"
                        print(line)
                        # GPSLat & GPSLon delivers position degrees, GPSHem and GPSMer provide hemisphere and side of meridian info
                        GPSLat = line[8:17]
                        GPSLon = line[20:30]
                        GPSHem = line[18:19]
                        GPSMer = line[31:32]
                        # Add hemisphere and meridian designation respectively in middle of position coordinates after degrees
                        Lat = GPSLat[:2] + GPSHem + GPSLat[2:]
                        Lon = GPSLon[:3] + GPSMer + GPSLon[3:]
                        UnitID=line[47:50]
			# Find UnitAlias from the dictionary referred by the UnitID number
       			UnitAlias=Unit_Aliases.get(UnitID)	
			output=('Unit %s (%s) reported position %s %s via %s' % (UnitID, UnitAlias, Lat, Lon, MsgProto))
			#logger.info('Raw message: ' + str(line))
			logger.info(output)
			#print(output)
			# Format the HTTP GET URL with variables
			httpget = ('http://havu.hylly.org/api/msg?msg=$POS|WGS84|%s|%s|%s|%s|%s|0|0*' % (UnitAlias, datenow, timenow, Lat, Lon))
			#print(httpget)	
			httprequest = requests.get(httpget)
			if httprequest.status_code == 200:
				SCOMS_status = ('SCOMS: ' + UnitAlias + ' position updated successfully')
			else:
				SCOMS_status = ('SCOMS: ' + UnitAlias + ' position update error. HTTP code ' + str(httprequest.status_code))
			logger.info(SCOMS_status)	
			#print httprequest.status_code	
			#print httprequest.headers
			#print httprequest.content

main()

ser.close()
