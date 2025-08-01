#!/usr/bin/env python3
# coding=utf-8
# ICE2APRS script (C) Georg Lukas DO1GL <georg@op-co.de>


import json
from datetime import datetime
from urllib2 import Request
from termcolor import colored
import socket
import sys
import time

VERSION="1.0"
SERVER="euro.aprs2.net"
INTERVAL=20 # minimum seconds between position posts
JSON_TRIP="https://portal.imice.de/api1/rs/tripInfo"
JSON_STATUS="https://portal.imice.de/api1/rs/status"

def get_json(url):
    loc = request.urlopen(url)
    if loc.status != 200:
        return None
    return json.loads(loc.read().decode())

def open_socket(call, passcode):
    LOGIN="user %s pass %s vers ICE2APRS.py %s\n" % (call, passcode, VERSION)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((SERVER, 14580))
    s.send(LOGIN.encode())
    return s

speed_record = 0

def post_loc(s, call, loc, comment):
    global speed_record

    lat = loc["latitude"]
    lon = loc["longitude"]
    kmh = int(loc["speed"])
    speed_record = max(kmh, speed_record)
    knots = int(kmh/1.852)
    timestamp = datetime.utcnow().strftime('%H%M%Sh')
    print(colored(loc, "yellow"))
    POS="%s-10>APRS:/%s%02d%05.2fN/%03d%05.2fE=   /%03d senk ju vor träwelling wis Deutsche Bahn (%s)\n" % \
        (call, timestamp, int(lat), (lat*60)%60,  int(lon), (lon*60)%60, knots, comment.strip())
    print(">>>", colored(POS.strip(), "red"))
    if lat != 0 and lon != 0:
        s.send(POS.encode())
    else:
        print("--- ignoring zero location")
    if speed_record > 0:
        print("--- speed record: %d km/h" % speed_record)


def get_trip_info():
    json = get_json(JSON_TRIP)
    return "%s-%s " % (json["trainType"],  json["vzn"])

def run(call, passcode):
    s = open_socket(call, passcode)
    last_ts = 0

    trip_info = get_trip_info()

    while True:
        t = time.time()
        if t > last_ts + INTERVAL:
            post_loc(s, call, get_json(JSON_STATUS), trip_info)
            last_ts = t
        try:
            for l in s.recv(2048).decode().split('\r\n'):
                print("<<<", colored(l, "green"))
        except socket.timeout:
            pass

    s.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Call me: %s CALL PASSCODE" % sys.argv[0])
    else:
        run(sys.argv[1], sys.argv[2])
