#!/usr/bin/env python3

import sys
import time

# Logging to see messages from networktables
import logging
logging.basicConfig(level=logging.DEBUG)

from networktables import NetworkTables


if len(sys.argv) != 2:
    print("Error: specify an IP to connect to!")
    exit(0)

ip = sys.argv[1]
NetworkTables.initialize(server=ip)
sd = NetworkTables.getTable("SmartDashboard")

i = 0
while True:
    try:
        print("robotTime:", sd.getNumber("robotTime"))
    except KeyError:
        print("robotTime: N/A")
    sd.putNumber("dsTime", i)
    time.sleep(1)
    i += 1
