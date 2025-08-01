# Radio tracking for FinRC events with Kenwood FM/DMR/NXDN radios
Purpose of the radio tracking is to provide position information of configured radios through VHF and visualize and track the position on a mapping platform

## Prerequisites
* Kenwood VHF radio (NX-3220E, NX-720GE or other GPS equipped radio which FinRC has in stock) for tracker stations
* Kenwood VHF radio (preferably a NX-720GE but any other will do as well) for receiving station of tracking messages + USB programming cable
* Computer running Traccar or similar tracking server

## Findings
Positive finding from NX-3220E handheld radio is that when configured to send GPS positions with fixed interval as status messages, the status messages are not sent over a voice channel reception. This was an issue earlier that the forced location transmission interrupted a received voice transmission and this confused the radio operators massively.

Traccar seems a good server side for the trackers, but has a lot of quirks and stupid things and things which have not been implemented at all. Good installation instructions for Traccar linux server here: https://electronica.bysmax.com/traccar/traccar/como-instalar-traccar-en-ubuntu-en-digitalocean

## Old stuff
The folder 'old stuff' includes earlier attempts to build a interface to receive position reports over USB serial port (Kenwood programming cable) using a Kenwood NX-720GE radio configured to receive the data messages (FleetSync-protocol)

This information could be useful building a new interface.

## NMEA and Kenwood-specific messages over the serial port

|Data|Description|
|:-|:-|
|$GPGGA (NMEA)|Upon receipt of the GPS data, the transceiver at the base station extracts the $GPGGA data in the NMEA-183 format from the received GPS data and sends the extracted data from the communication port.<br/>[$GPGGA sentence explained](https://aprs.gids.nl/nmea/#gga)|
|$GPGLL (NMEA)|Upon receipt of the GPS data, the transceiver at the base station extracts the $GPGLL data in the NMEA-183 format from the received GPS data and sends the extracted data from the communication port.<br/>[$GPGLL sentence explained](https://aprs.gids.nl/nmea/#gll)|
|$GPRMC (NMEA)|Upon receipt of the GPS data, the transceiver at the base station extracts the $GPRMC data in the NMEA-183 format from the received GPS data and sends the extracted data from the communication port.<br/>[$GPRMC sentence explained](https://aprs.gids.nl/nmea/#rmc)|
|-|-|
|$PKNDS (Kenwood)|Upon receipt of the GPS data, the transceiver at the base station creates the $PKNDS data which is the Kenwood proprietary sentence from the received GPS data and sends the created data from the communication port. The $PKNDS data contains the $GPRMC data in the NMEA-0183 format, Unit ID, and the status information.|
|$PKNID (Kenwood)|Upon receipt of the GPS data, the transceiver at the base station creates the $PKNID data which is the Kenwood proprietary sentence from the received GPS data and sends the created data from the communication port. The transceiver at the base station extracts only Unit ID and the status information from the received GPS data and sends the extracted data from the communication port of the repeater. This sentence is recommended to be used along with $GPGGA (NMEA), $GPGLL (NMEA) or $GPRMC (NMEA).<P/>For example, if $GPGGA (NMEA) and $PKNID are used simultaneously, the transceiver at the base station sends from the communication port of the repeater the $GPGGA data in addition to the Unit ID and the status information extracted from the GPS data.|
|$PKNSH (Kenwood)|Upon receipt of the GPS data, the transceiver at the base station creates the $PKNSH data which is the Kenwood proprietary sentence from the received GPS data and sends the created data from the communication port. The $PKNSH data contains the $GPGLL data in the NMEA-0183 format and the Unit ID. In order to send GPS data in Emergency Mode or by pressing the PTT switch, this sentence is used.|
