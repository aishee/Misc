#!/usr/bin/env python
import socket, sys, argparse
#resolve host
def resolve(host):
    try:
        address = socket.gethostbyname(host)
        return address
    except:
        print '[+] - Host is error'
        exit()
    
#Port scan function
def scanPort(address, start, end):
    c = 0
    if start >= end:
        print '[+] Please check input start and end variales'
        exit()
    for port in range(start, end):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        r = s.connect_ex((address, port))
        s.close()
        if r == 0:
            print '[+] - Port ', port, ' is open'
            c = c + 1
    return c

if __name__ == '__main__':
    #parser section
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Host to check doors")
    parser.add_argument("-m", "--min", help="Port to start check", type=int)
    parser.add_argument("-M" , "--max", help="Port to finish check", type=int)
    args = parser.parse_args()
    
    #Variables
    count = 0
    start = 1
    end = 1024
    
    #Main
    try:
        ip = resolve(args.host)
        print '[+] - Checking %s / %s'%(args.host, ip)
        
        if args.min:
            start = args.min
        if args.max:
            end = args.max
        count = scanPort(ip,start, end)
        print '[+] - Found ', count, 'open doors'
        print '[+] - Completed successfully'
    except KeyboardInterrupt:
        print
        print '[+] - Interrupted scan'
        print '[+] - Was found ', count, 'open doors before finish it'
        