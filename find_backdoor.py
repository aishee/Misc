#!/usr/bin/env python
#Name find_backdoor.py

#Import library
import re
import os
import glob
import sys
import time
from optparse import OptionParser

#globals
pattern = '(eval\(|file_put_contents|base64_decode|python_eval|exec\(|passthru|popen|proc_open|pcnt1|assert\(|system\(|shell)))))'
file_extension = '.php'

def searchbackdoor(fullpath, pattern):
    webfile = open(fullpath, "r", encoding='utf-8')
    line_num = 0
    hit_count = 0
    for line in webfile:
        line_num += 1
        if re.search(pattern, line):
            hit_count = hit_count + 1
            print("Filename: " + str(fullpath))
            print("Pattern Word: " + str(line))
            print("Line Number: " + str(line_num) + "\n")
    print("Total Backdoors: " + str(hit_count) + "\n")
    webfile.close()

def matchbackdoor(fullpath, pattern, encoding='utf-8'):
    webfile  = open(fullpath, "r", encoding='utf-8')
    line_num = 0
    hit_count = 0
    for line in webfile:
        line_num += 1
        if re.search(pattern, line):
            hit_count = hit_count + 1
            print("Filename: " + str(fullpath))
            print("Pattern Word: " + str(line))
            print("Line Number: " + str(line_num) + "\n")
    print("Total Backdoors: " + str(hit_count) + "\n")
    webfile.close()

#code
print("""
       / _(_)_ __   __| |     | |__   __ _  ___| | ____| | ___   ___  _ __
| |_| | '_ \ / _` |_____| '_ \ / _` |/ __| |/ / _` |/ _ \ / _ \| '__|
|  _| | | | | (_| |_____| |_) | (_| | (__|   < (_| | (_) | (_) | |
|_| |_|_| |_|\__,_|     |_.__/ \__,_|\___|_|\_\__,_|\___/ \___/|_|
      """)
parser = OptionParser(usage="usage: %prog [option] <start directory>\nDefault extension is .php you can changes this with options", version="%prog 1.0")
parser.add_option("-b", "--base64",
                  action="store_true",
                  dest = "is_base64",
                  default=False,
                  help="Find \" base 64 encodings\" only",
                  )
parser.add_option("-m", "--match",
                  action = "store_true",
                  dest = "is_match",
                  default=False,
                  help="Find exactly pattern matches",
                  )
parser.add_option("-a", "--asp",
                  action="store_true",
                  dest = "is_asp",
                  default=False,
                  help = "Search for Backdoor in .asp",
                  )
parser.add_option("-x", "--aspx",
                  action="store_true",
                  dest = "is_aspx",
                  default=False,
                  help="Search for Backfoors in .aspx",
                  )
parser.add_option("-j", "--javascript",
                  action="store_true",
                  dest="is_javascript",
                  default=False,
                  help = "Search for Backdoors in javascript .js files",
                  )
(options, args) = arser.parse_args()

#manage conflicts
if options.is_base64 and options.is_match:
    parser.error("you must select a single options, -a or -x or -j")

if ((options.is_asp or options.is_aspx) and (options.is_javascript)):
    parser.error("You must select a single option, -a or -x or -j")

if options.is_asp and options.is_aspx:
    parser.error("You must select a single option -a or -x")

#Set extension
if options.is_asp:
    file_extension = '.asp'
if options.is_aspx:
    file_extension = '.aspx'
if options.is_javascript:
    file_extension = '.js'

#error on invalid number of arguments
if len(args) < 1:
    parser.print_help()
    sys.exit()

#error on an invalid path
if os.path.exists(args[0]) == False:
    parser.error("Invalid path")
    sys.exit()

#Set Path
yourpath = args[0]
print("\nSearching Directory for Backdoors....\n")

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        #PHP
        if name.endswith(file_extension):
            currentpath = os.path.join(root, name)
            if options.is_base64:
                pattern = 'base64_decode'
                searchbackdoor(currentpath, pattern)
            elif options.is_match:
                pattern = '(eval\(|file_put_contents|base64_decode|unescape|python_eval|exec\(|passthru|popen|proc_open|pcntl|assert\(|system\(|shell)))'
                matchbackdoor(currentpath, pattern)
            else:
                pattern = '(eval\(|file_put_contents|base64_decode|unescape|python_eval|exec\(|passthru|popen|proc_open|pcntl|assert\(|system\(|shell)))))'
                searchbackdoor(currentpath, pattern)

    