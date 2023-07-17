# Demo

This repository contains smaller projects used for the demonstrations at Berlin 6G Conference in July 2023 as well as the HPI Bachelorpodium. The demo consists of captive portal, lights on the APs to visualize the VXLANs and a web app to let a linux client roam.

## roamer and roamer-reconnect

These tools provide a web interface that can be used to control `wpa-cli` on a Linux laptop to show the roaming process between two APs.
This code is specific to the laptop we used for the demonstration. For this reason, you may need to modify the `wlan_iface` variable in the file `app/main.py`.
In addition, you may also want to modify the MAC addresses and names of the used APs.

To start the server, first install the requirements using `pip` and the `requirements.txt` file.
Then run the following commands:

```bash
cd app
sudo uvicorn main:app --reload
```

> When setting up the demonstration, we noticed a [Bug in FRR](https://github.com/FRRouting/frr/issues/13973) which results in connectivity issues after a roam.
> To still show movement between APs, we decided to modify the code located in `roamer` to first disconnect from the old and then reconnect to the new AP and placed that code in `roamer-reconnect`. It can be used the same way.

## portal

This is a captive portal that can be run on the gateway server to show users which virtual network they are in and what AP they are connected to.

To run the portal, you first need to install all dependencies using `npm i` and then build the typescript project using `npm build`.
You can then run the code by using

```bash
sudo ./run.sh
```

> Please note again that this code is very specific to the demo setup.
> The IPv4 address of the connected client is used to determine the VNI that it is connected to.
> In addition, it supports exactly three networks (VNI 1,2,3) which are represented by the colors red, green, and blue.

## Lights on the APs

The setup consists of two components. One daemon running on the AP parsing vtysh and generating the light sequence and the code on the arduino receiving the light sequence and controlling the LEDs accordingly. For the arduinos to work with openWrt a guide with the packages to install can be found [here](https://openwrt.org/docs/guide-user/advanced/arduino)

### Blinken

Blinken is a python script that queries `vtysh` and sends out lighting commands via serial. Every command is a sequence of 8 hex values. One hex value for each LED. Use `install.sh` to install the script and an init file onto the access point. The first positional argument is the ssh host. Additionally the packages `python3-light python3-pyserial` are needed on the access point.

### aplight

This code is the code that is run on the Arduino Nano microcontrollers connected to the APs via USB.
It receives the color values as hexadecimal colors via Serial and shows them in a rotating animation.
A 12-LED ring of WS2812 RGB LEDs ("NeoPixel") is connected to PIN 3 of the Arduino.

The whole project is a [platform.io](https://platformio.org/) project, so it is advisable to install the platform.io IDE and follow its documentation to compile and upload the code to an Arduino.
