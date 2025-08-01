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
