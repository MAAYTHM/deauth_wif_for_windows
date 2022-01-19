# deauth_wifi
A Python3 tool, which simply sends ∞ deauth packets to victim becoz of which victim device cannot able to connect to wifi

**`Tool is in Development`**

**Only '`-i`', '`-l`', '`-C`' options are working now**


### help menu :-
```python
usage: deauth_wifi.py [-h] [-i INTERFACE] [-c COUNT] [-b BSSID] [-l]
                      [-t MAC addr] [-C]

A Python3 tool, which simply sends ∞ deauth packets to wifi becoz of which victim device cannot able to connect to wifi

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        interface to select ,for searching available Access
                        Points. Run this tool without any option to look for
                        available interfaces
  -c COUNT, --count COUNT
                        The number of deauthentication packets to send to
                        victim (default - ∞)
  -b BSSID, --bssid BSSID
                        BSSID of a Access Point
  -l, --list            List info about all available Access Points. Use it
                        with "-i" for specific interface's Access Points.
  -t MAC addr, --target MAC addr
                        MAC address of target
  -C, --color           Colorize Output

Additional Information :
    * It is Python3 tool.
    * If you want to use any option other than '-C' then it is preferred that Run the program with 'Admin shell/privilege'.
    * Give value to options in double quotes, like - 'python deauth_wifi.py -i "Wi-Fi" -l'.
    * After pressing 'Ctrl+C', while listing SSID's , please wait 1-2 sec.

example usage :
     python deauth_wifi.py
     python deauth_wifi.py -i "Wi-Fi" -
```
