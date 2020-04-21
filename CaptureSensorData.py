# -*- coding: utf-8 -*-
import json
import serial
import sys
import time
import csv

port = "COM3"

baudrate = 115200

if len(sys.argv) == 3:
    ser = serial.Serial(sys.argv[1], sys.argv[2])
else:
    print("# Please specify a port and a baudrate")
    print("# using hard coded defaults " + port + " " + str(baudrate))
    ser = serial.Serial(port, baudrate)

# enforce a reset before we really start
#ser.setDTR(1)
#time.sleep(0.25)
#ser.setDTR(0)

while 1:
    print(ser.readline())