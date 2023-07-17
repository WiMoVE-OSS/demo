# demo

This repository contains smaller projects used for the demonstrations at Berlin 6G Conference in July 2023 as well as the HPI Bachelorpodium.

## roamer and roamer-reconnect

These tools provide a web interface that can be used to control `wpa-cli` on a Linux laptop to show the roaming process between two APs.
This code is specific to the laptop we used for the demonstration. For this reason, you may need to modify the `wlan_iface` variable in the file `app/main.py`.

To start the server, first install the requirements using `pip` and the `requirements.txt` file.
Then run the following commands:

```bash
cd app
sudo uvicorn main:app --reload
```

> When setting up the demonstration, we noticed á [Bug in FRR](https://github.com/FRRouting/frr/issues/13973) which results in connectivity issues after a roam.
> To still show movement between APs, we decided to modify the code located in `roamer` to first disconnect from the old and then reconnect to the new AP and placed that code in `roamer-reconnect`. It can be used the same way.
