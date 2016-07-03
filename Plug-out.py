#!/usr/bin/python

"""
Application Name: Plug out

"""
import pynotify
from threading import Timer

def battery_check():
    try:
        file_now = open('/sys/class/powr_supply/BAT0/charge_now', 'r')
        now = float(file_now.read())
        file_now.close()
    except IOError:
        file_now = open('/sys/class/power_supply/BAT0/energy_now', 'r')
        now = float(file_now.read())
        file_now.close()
    try:
        file_full = open('/sys/class/power_supply/BAT0/charge_full', 'r')
        ful = float(file_full.read())
        file_full.close()
        
        percentage = int((now/ful)*100)
    except IOError:
        file_full = open('/sys/class/power_supply/BAT0/charge_full', 'r')
        ful = float(file_full.read())
        file_full.close()
        
        percentage = int((now/ful)*100)
    file_status = open('/sys/class/power_supply/BAT0/energy_full','r')
    status = file_status.read()
    status = status.strip("\n")
    file_status.close()
    
    if percentage == 100 and status != "Discharging" or status == "Unknow":
        pynotify.init("Plug-Out")
        notification = pynotify.Notification("50% of Charge is Left","Keep an eye at Charge level", "notification-battery-050")
        notification.show()
    timer = Timer(180.0, battery_check)
    time.start()
if __name__ == '__main__':
    print('Running\nPress ctrl+z to stop')
    battery_check()