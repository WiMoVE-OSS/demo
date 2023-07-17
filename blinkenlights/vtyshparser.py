#!/usr/bin/env python3
import json
from collections import defaultdict
import serial
from time import sleep
import os

SERIAL_PORT_PREFIX = "/dev/ttyUSB"

COLORS = ["ff0000", "00ff00", "0000ff"]
DEFAULT_COLOR = "000000"
MAX_VNI = len(COLORS)
MAX_CLIENTS = 4
NUM_PIXELS_PER_COLOR = 4


print("Waiting for port to become ready")
while True:
    serial_port = os.popen(f"ls {SERIAL_PORT_PREFIX}*").read().strip()
    try:
        with serial.Serial(serial_port, 9600) as ser:
            sleep(5)
            print("Starting.")
            while True:

                output = []

                string = os.popen('vtysh -c "show evpn mac vni all json"')
                #string = open("sample.json")
                data = json.load(string)

                counter = defaultdict(int)

                for key, value in data.items():
                    macs = value['macs']
                    for mac in macs.values():
                        if mac["type"] == "local":
                            counter[key] += 1


                for i in range(1, MAX_VNI + 1):
                    value = counter[str(i)]
                    for j in range(NUM_PIXELS_PER_COLOR):
                        if j < value:
                            output.append(COLORS[i - 1])
                        else:
                            output.append(DEFAULT_COLOR)

                print(output)
                print(" ".join(output))

                string = " ".join(output) + " \n"
                ser.write(string.encode("ascii"))
                print("Waiting for next round")
                sleep(3)
    except serial.serialutil.SerialException as e:
        print(e)
        print("Retrying")
        sleep(1)
