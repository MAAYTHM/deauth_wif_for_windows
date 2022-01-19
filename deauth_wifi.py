# Summary - It simply sends ∞ deauth packets to wifi becoz of which any device cannot able to connect to that wifi

# Module Requirements :-
    # scapy
    # subprocess
    # re
    # argparse
    # sys
    # columnar
    # Jinja2
    # os
    # ctypes

# importing main modules
import scapy.all as scapy # for sending spoofed deauth packets
import subprocess # for executing system cmds
import re # for using regular expressions

# For cmdline functionality
from argparse import ArgumentParser as AP, RawDescriptionHelpFormatter as RDF

# for exiting the program safely
import sys

# for checking admin privilege
import os
import ctypes



                                                                        # FUNCTIONS AREA STARTS


# function to print logo at starting
def logo(allow=False): # disabling colors for terminals which does not support colors (by default) :

    # calling global variable
    global blue, red, red_bold, yellow, green, default_, orange, white, pink, yellow_bold, yellow_italic, pink_bold, white_underline, white_bold, black_white_bg

    # Color codes For banner
    if allow:
        blue = '\033[36m'
        red = '\33[31m'
        red_bold = '\33[1;31m'
        yellow = '\33[33m'
        yellow_bold = '\033[1;33m'
        yellow_italic = '\033[3;33m'
        green = '\33[32m'
        default_ = '\33[m'
        orange = '\033[1;38;2;255;165;0m'
        white = '\033[37m'
        white_underline = '\033[2;37m'
        white_bold = '\033[1;37m'
        black_white_bg = '\033[2;30;47m'
        pink = '\033[35m'
        pink_bold = '\033[1;35m'

    # Banner
    print(
    '\n\n' + 
    blue    + r"""███╗   ███╗ █████╗  █████╗ ██╗   ██╗""" + "\n" +
    red     + r"""████╗ ████║██╔══██╗██╔══██╗╚██╗ ██╔╝""" + "\n" +
    yellow  + r"""██╔████╔██║███████║███████║ ╚████╔╝"""+ "\n" +
    yellow  + r"""██║╚██╔╝██║██╔══██║██╔══██║  ╚██╔╝""" + "\n" +
    red     + r"""██║ ╚═╝ ██║██║  ██║██║  ██║   ██║""" + "\n" +
    blue    + r"""╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝""" + default_ + '\n')

    print()
    print(yellow_italic + "****************************************************************")
    print("* Copyright of MAAY, 2022                                      *")
    print("* https://github.com/MAAYTHM                                   *")
    print("* https://tryhackme.com/p/MAAY                                 *")
    print("****************************************************************" + default_)
    print()


# Check IF it is running with admin privilege or not?
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


# 'multi_into_1' function will convert dictionary values into 1 single line / single string
# eg :-
    # input -> [{'ssid': '', 'channel': '149', 'bssid': '11:11:11:11:11:11', 'band': '5 GHz', 'authentication': 'WPA2-Personal', 'signal': '78% '}, {'ssid': '', 'channel': '149', 'bssid': '22:22:22:22:22:22', 'band': '5 GHz', 'authentication': 'WPA2-Personal', 'signal': '78%'}]
    
    # output :-
    #    ''      149    11:11:11:11:11:11   5 GHz   WPA2-Personal   78%
    #    ''      149    22:22:22:22:22:22   5 GHz   WPA2-Personal   78%

def multi_into_1(dict1, ssid_max_len, cha_max_len, bssid_max_len, band_max_len, auth_max_len, sig_max_len):

    # global color variables
    global yellow, green, default_, blue, red_bold, orange, pink

    string = ''
    
    # Handling each dictionary item in list
    for i in dict1:

        # numeric value of signal
        numeric_signal = int(i["signal"][:-1])

        # creating padded variables to print
        ssid = i['ssid'].center(ssid_max_len)
        channel = i['channel'].center(cha_max_len)
        bssid = i['bssid'].center(bssid_max_len)
        band = i['band'].center(band_max_len)
        authentication = i['authentication'].center(auth_max_len)
        signal = i['signal'].center(sig_max_len)

        # adding colors , according to conditions
        if not ssid.isspace():
            ssid = blue + ssid + default_
        
        if 'Open' in authentication:
            authentication = green + authentication + default_
        else:
            authentication = red_bold + authentication + default_
        
        if numeric_signal >= 70:
            signal = green + signal + default_
        elif numeric_signal >= 50:
            signal = yellow + signal + default_
        elif numeric_signal >= 25:
            signal = orange + signal + default_
        else:
            signal = red_bold + signal + default_
        
        bssid = pink + bssid + default_

        # adding padded variables with new line character
        string += ssid
        string += channel
        string += bssid
        string += band
        string += authentication
        string += signal
        string += '\n'

    return string



# function to get all wireless interfaces, it will return list of all interfaces :
def get_interfaces():

    # final list which store all interfaces name and descriptions
    final_list_interfaces = []

    # Getting interfaces list:
    cmd = 'netsh wlan show interface'.split()
    output = subprocess.run(cmd, capture_output=True).stdout.decode()
    all_interfaces = re.findall('Name                   : (.*)\r', output)

    # Max length bw all interface and description
    max_interface_len = 0
    max_description_len = 0

    # Checking if there is no interfaces :
    if not all_interfaces:
        return []
    
    # Fetching description of each wireless interface :
    for interface in all_interfaces:
        cmd = f'netsh wlan show interface name="{interface}"'.split()
        output = subprocess.run(cmd, capture_output=True).stdout.decode()
        int_description = re.findall('Description            : (.*)\r', output)[0]

        # assigning max length
        if len(interface) > max_interface_len:
            max_interface_len = len(interface)
        
        if len(int_description) > max_description_len:
            max_description_len = len(int_description)
        
        # Appending interface_name, description in final_list_interfaces :
        final_list_interfaces.append([interface, int_description])
    
    # returning an interface list and max length
    return [final_list_interfaces, [max_interface_len, max_description_len]]


# function to get all SSID's available on an interface
def get_ssids(interface):
    all_ssid = []

    # Feteching SSID's and their info
    cmd = f'netsh wlan show networks interface="{interface}" mode=bssid'.split()
    output = subprocess.run(cmd, capture_output=True).stdout.decode()
    all_ssid = re.findall('SSID ([0-9]+) : (.*)\r', output)
    check = False
    
    d = {} 
    # d[bssid] = {'ssid': ssid, 'channel':'', 'bssid': '', 'band':'', 'authentication': '', 'signal': ''} # format of a column in dict

    for i in all_ssid: # i[0] - index, i[1] - ssid_name

        # variables to use
        index = i[0]
        ssid = i[1]
        total_bssid = 1
        auth = ''
        list_bssid = []

        for i in output.split('\n'):

            # Check = True, means We are in bw two SSID's contents. like :-
            # SSID 1 : one
                # Network type            : Infrastructure
                # Authentication          : WPA2-Personal
                # Encryption              : CCMP
            # SSID 2 : two

            # You can see above, ['Network type', 'Authentication', 'Encryption'] are in between 2 SSID's

            if f'SSID {index} : ' in i and 'BSSID' not in i:
                check = True
            
            if f'SSID {int(index)+1} : ' in i and 'BSSID' not in i:
                check = False
                break

            if check: # means bw 2 ssid's column

                # bssid stuff
                bssid_number = re.findall('BSSID ([0-9]+)                 : .*\r', i)
                if bssid_number:
                    bssid = re.findall('BSSID [0-9]+                 : (.*)\r', i)[0]
                    bssid_number = bssid_number[0]

                    try :
                        d[bssid]
                    except Exception as e:
                        # Creating new dict for each 'bssid'
                        d[bssid] = {'ssid': ssid, 'channel':'', 'bssid': bssid, 'band':'', 'authentication': '', 'signal': ''}

                    if int(bssid_number) > total_bssid:
                        total_bssid += 1
                    
                    if bssid not in list_bssid: list_bssid.append(bssid)
                
                # channel number
                elif 'Channel' in i and 'Channel Utilization' not in i:
                    channel = re.findall('Channel            : (.*) \r', i)[0]
                    d[bssid]['channel'] = channel
                
                # bandwidth
                elif 'Band' in i:
                    band = re.findall(' Band               : (.*)\r', i)[0]
                    d[bssid]['band'] = band

                # authentication
                elif 'Authentication' in i:
                    auth = re.findall('Authentication          : (.*)\r', i)[0]

                # signal
                elif 'Signal' in i:
                    signal = re.findall('Signal             : (.*) \r', i)[0][:-1]
                    d[str(bssid)]['signal'] = signal
        
        # updating auth column in every list in 'last ssid'
        for i in list_bssid:
            d[i]['authentication'] = auth

    # Modifying the 'd' dictionary to a list
    # previous 'd' - {'11:11:11:11:11:11': {'ssid': '', 'channel': '149', 'bssid': '11:11:11:11:11:11', 'band': '5 GHz', 'authentication': 'WPA2-Personal', 'signal': '78% '}, '22:22:22:22:22:22': {'ssid': '', 'channel': '149', 'bssid': '22:22:22:22:22:22', 'band': '5 GHz', 'authentication': 'WPA2-Personal', 'signal': '78%'}}
    # new 'd' - [{'ssid': '', 'channel': '149', 'bssid': '11:11:11:11:11:11', 'band': '5 GHz', 'authentication': 'WPA2-Personal', 'signal': '78% '}, {'ssid': '', 'channel': '149', 'bssid': '22:22:22:22:22:22', 'band': '5 GHz', 'authentication': 'WPA2-Personal', 'signal': '78%'}]
    new_d = []
    for keys in d:
        new_d.append(d[keys])

    # total number of lines, which we will be printed in ∞ loop
    total_index = len(new_d)

    
                                    ### Printing Available SSID's in proper manner

    # Padding length
    ssid_max_len = 30 # for ssid column padding
    bssid_max_len = 20 # for bssid column padding
    auth_max_len = 20 # for authentication column padding
    band_max_len = 10 # for band column padding
    sig_max_len = 10 # for signal column padding
    cha_max_len = 10 # for channel column padding

    result = multi_into_1(new_d, ssid_max_len, cha_max_len, bssid_max_len, band_max_len, auth_max_len, sig_max_len)

    # Printing SSID :
    return [result, total_index]
    

# function for displaying error messages
def error_(msg):

    # gloabl color variables
    global red_bold, default_

    # If user exit then make sure to enable the interface
    cmd = f'netsh interface set interface name="{given_interface}" admin=enabled'.split()
    subprocess.run(cmd, capture_output=True).stdout.decode()

    # printing errors
    print('\n' + red_bold + msg + default_ + '\n')
    sys.exit()


# function to write info messages
def info_(msg):

    # global color variables
    global white_bold, default_

    # printing info messages :
    print('' + white_bold + msg + default_ + '')



                                                                        # FUNCTIONS AREA FINISHED



# global variables for colors :
blue = ''
red = ''
red_bold = ''
yellow = ''
green = ''
default_ = ''
orange = ''
white = ''
white_underline = ''
white_bold = ''
black_white_bg = ''
pink = ''
yellow_bold = ''
yellow_italic = ''
pink_bold = ''


# Argument parser initializer
description = "A Python3 tool, which simply sends ∞ deauth packets to wifi becoz of which victim device cannot able to connect to wifi"
epilog = '''
Additional Information :
    * It is Python3 tool.
    * If you want to use any option other than '-C' then it is preferred that Run the program with 'Admin shell/privilege'.
    * Give value to options in double quotes, like - 'python deauth_wifi.py -i "Wi-Fi" -l'.
    * After pressing 'Ctrl+C', while listing SSID's , please wait 1-2 sec.

example usage :
     python deauth_wifi.py
     python deauth_wifi.py -i "Wi-Fi" -l
'''
parser = AP(description=description, epilog= epilog, formatter_class=RDF)

# Adding cmdline arguments
parser.add_argument('-i', '--interface', help='interface to select ,for searching available Access Points. Run this tool without any option to look for available interfaces')
parser.add_argument('-c', '--count', help='The number of deauthentication packets to send to victim (default - ∞)')
parser.add_argument('-b', '--bssid', help='BSSID of a Access Point')
parser.add_argument('-l', '--list', action='store_true', help='''List info about all available Access Points. Use it with "-i" for specific interface's Access Points.''')
parser.add_argument('-t', '--target', metavar='MAC addr', help='MAC address of target')
parser.add_argument('-C', '--color', action='store_true', help='Colorize Output')


# Getting arguments values from cmdline
args = parser.parse_args()

# Exceuting cmds as per user setted options
try:

    # Commands line arguments functions :

    # allowing colors
    if args.color:
        colors_allow = True
        logo(colors_allow)
    
    # not allowing colors
    else:
        logo()

    if args.interface or args.count or args.bssid or args.list or args.target:

        if isAdmin(): # check first at starting, that it is running with admin privilege or not

            # Checking for "-l" option is set or not?
            if args.list:
                
                # If only '-l' options is not there, like - 'deauth_wifi.py -l -i <interface>'
                if args.interface and not args.count and not args.bssid and not args.target:
                
                    # Finding available Access Points :
                    given_interface = args.interface

                    # Checking if there is any interface :
                    all_interfaces = get_interfaces()
                    all_interfaces = all_interfaces[0]
                    if not all_interfaces:
                        error_('No Interfaces were FOUND !!')
                    
                    # List of actual interfaces
                    actual_interfaces = []
                    for interface in all_interfaces:
                        actual_interfaces.append(str(interface[0]))

                    # Checking if given_interface exists or not :
                    if str(given_interface) not in actual_interfaces:
                        error_('''Wrong Interface is given !!    OR    '-i' value should be in double quotes !!''')

                    # Printing Interface :
                    info_(f'Interface Name - {given_interface}')
                    info_('''[ If ssid is blank then it means that Access Point's SSID is "hidden" ]''')
                    print()

                    
                                                        ### Starting finding and printing SSIDS
                    

                    # Headers with custom padding
                    print(black_white_bg + 'SSID'.center(30) + 'CHANNEL'.center(10) + 'BSSID'.center(20) + 'BAND'.center(10) + 'AUTHENTICATION'.center(20) + 'SIGNAL'.center(10) + default_)

                    # ∞ loop
                    try:
                        while True:

                            # getting list of ssids
                            # list_[0] = SSID's list
                            # list_[1] = total number of lines which we have to print
                            list_ = get_ssids(given_interface)

                            # If there is no ssids then , obviously we will print nothing and if print nothing then we do not need to delete last printed line:
                            if list_[1] != 0:

                                # variables for clearing last printed lines
                                line_up = f'\033[1A'
                                line_clear = '\x1b[2K'

                                # Printing SSIDS
                                print(list_[0])
                                
                                # line deleted variable, it will be true once previous lines are deleted in ∞ loop, it will be false when lines are printed
                                line_deleted = False
                                
                                # reresh the wifi via disabling and enabling
                                cmd = f'netsh interface set interface name="{given_interface}" admin=disabled'.split()
                                subprocess.run(cmd, capture_output=True).stdout.decode()

                                cmd = f'netsh interface set interface name="{given_interface}" admin=enabled'.split()
                                subprocess.run(cmd, capture_output=True).stdout.decode()

                                # Clearing previous printed lines :
                                for i in range(list_[1]+1):
                                    print(line_up, end=line_clear)
                                
                                # set = True, once line is deleted
                                line_deleted = True
                            
                    # If Ctrl+C pressed during ∞ loop
                    except KeyboardInterrupt:
                        
                        print(red_bold + 'Ctrl-C Pressed!!' + default_)
                        info_('Enabling interface if it is down, plz wait few secs...')
                        # ctrl+c pressed after lines deleted
                        if line_deleted:
                            print(list_[0])
                        error_('Program exits ...')


                else:
                    print(red_bold + "'-l' should use with '-i' only" + default_ + '\n')
                    sys.exit()

            # if any other option :-
            else:
                info_('Tool is in Development now, Sorry!!\n')
                sys.exit()

        else:
            error_('Run as ADMIN!!')

    
    # By default, Printing all available interfaces in system :
    else:
        
        # calling get_interfaces function , to get list of available interfaces
        final_list_interfaces = get_interfaces()
        # final_list_interfaces[0] - interface list
        # final_list_interfaces[1][0] - max interface len
        # final_list_interfaces[1][1] - max description len


        # Checking if there is no interface
        if not final_list_interfaces[0]:
            error_('No Interfaces were FOUND !!')
        
        else:
            # max lengths :-
            max_interface_len = 20
            max_description_len = 30

            if final_list_interfaces[1][0] > max_interface_len:
                max_interface_len = final_list_interfaces[1][0] + 4
            
            if final_list_interfaces[1][1] > max_description_len:
                max_description_len = final_list_interfaces[1][1] + 4


            # Printing column headers :
            titles = pink_bold + ' Interface Name '.center(max_interface_len) + default_ + yellow_bold + ' Description '.center(max_description_len) + default_
            print(titles)
            
            # Printing rows :
            for row in final_list_interfaces[0]:
                print(yellow_bold + row[0].center(max_interface_len) + pink_bold + row[1].center(max_description_len) + default_)
            
            print()

except Exception as e:
    error_(e)

