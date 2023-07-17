#!/bin/bash
scp -O vtyshparser.py "$1":/usr/bin/blinken.py 
scp -O blinken "$1":/etc/init.d/blinken
ssh "$1" "chmod +x /etc/init.d/blinken"
ssh "$1" "chmod +x /usr/bin/blinken.py"
ssh "$1" service blinken enable
ssh "$1" service blinken start
