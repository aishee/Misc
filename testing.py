#!/usr/bin/env python3.5

import subprocess
import csv
import platform
import colorama
from colorama import Back, Fore, Style

def ping(hostname):
    if platform.system() == "Windows":
        p = subprocess.Popen('ping ' + hostname + " -n 1", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen('ping -c 1 ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pingStatus = 'ok'
    for line in p:
        output = line.rstrip().decode('UTF-8')
        
        if (output.endswith('unreachable.')):
            #No route from the local system. Packets sent were never put on the wire.
            pingStatus = 'unreachable'
            break
        elif (output.startswith('Ping resquest cuold not find host')):
              pingStatus = 'host_not_found'
              break
        if (output.startswith('Request timed out.')):
        #no echo reply message were received within the default time of 1 second
            pingStatus = 'timed_out'
            break
    return pingStatus

def printPingResult(hostname):
    stautsOfPing = ping(hostname)
    if (statusOfPing == 'host_not_found'):
        print(Fore.WHITE + Back.RED + hostname +" Host not found" + Style.RESET_ALL)
    elif (statusOfPing == 'unreachable'):
        print(Fore.WHITE + Back.RED + hostname + " Unreachable " + Style.RESET_ALL)
    elif (statusOfPing == 'timed_out'):
        print(Fore.WHITE + Back.RED + hostname + " Time Out " + Style.RESET_ALL)
    elif (stautsOfPing == 'ok'):
        print(Fore.GREEN + hostname + " OK " + Style.RESET_ALL)

if __name__ == '__main__':
    server = open('server.txt', 'r')
    try:
        reader = csv.reader(server)
        for item in reader:
            printPingResult(item[0].strip())
    finally:
        server.close()