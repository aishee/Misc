#!//usr/bin/python
# -*- coding: utf-8 -*-


from cmd2 import Cmd, make_option, options
from optparse import OptionParser
from scapy.all import *
import sys
import re

class bcolors:
    HEADER = '\033[95m'
    PROMPT = '\033[94m'
    TXT = '\033[93m'
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    ENDC = '\033[0m'

class Forensic(Cmd):
    def __init__(self, namefile):
        Cmd.__init__(self)
        self.last = []
        self.last.append([])
        self.prompt = bcolors.PROMPT  + "ForPCAP >>> " + bcolors.ENDC
        self.localPcap(namefile)
        self.cmd = ""

    def loadPcap(self, namefile):
        sys.stdout.write(bcolors.TXT + "## Loading PCAP " + namefile + " ... ")
        sys.stdout.flush()
        self.pcap = rdpcap(namefile)
        sys.stdout.write("OK." + bcolors.ENDC + "\n")
        self.last = self.pcap

    def do_version(self, arg, opts=None):
        """Print version of forensic"""
        print bcolors.TXT + "Forensic PCAP v0.2 written by Aishee"

    def do_dns(self, arg, opts=None):
        """Print all DNS requests in the PCAP file
        Usage:
         - ports"""
         sys.stdout.write(bcolors.TXT + "## Listing all destination port in the PCAP...")
         sys.stdout.flush()
         ports = []
         ports.append([])
         for i, packet in enumerate(self.pcap):
             if TCP in packet:
                 res = packet.getlayer('TCP').dport()
                 test = 0
                 for port in ports:
                     if len(port) == 2:
                         if int(res) == int(port[1]):
                             test = 1
                             break
                if test == 0:
                    ports.append([i, res])
        sys.stdout.write("OK.\n")
        print bcolors.TXT + "Result : " + str(len(ports) - 1) + " ports##" + bcolors.ENDC
        self.last = ports
        self.cmd = "dstports"

    def do_stat(self, arg, opts=None):
          """Print stats about PCAP
         Usage:
          -stat """
        sys.stdout.write(bcolors.TXT + "## Calculating statistics about the PCAP...")
        sys.stdout.flush()
        tcp = 0
        udp = 0
        arp = 0
        icmp = 0
        other = 0
        for packet in self.pcap:
            if TCP in packet:
                tcp = tcp + 1
            elif UDP in packet:
                udp = udp + 1
            elif ARP in packet:
                arp = arp + 1
            elif ICMP in packet:
                icmp = icmp + 1
            else:
                other = other +1
        sys.stdout.write("OK.\n" + bcolors.ENDC)
        print "## Statistics: "
        print "TCP : " + str(tcp) + " packet(s)"
        print "UDP : " + str(udp) + " packet(s)"
        print "ARP : " + str(arp) + " packet(s)"
        print "ICMP : " + str(icmp) + " packet(s)"
        print "Other: " + str(other) + " packet(s)"
        print "Total: " + str(other) + " packet(s)"
        print "## End of statistics"

        self.cmd = "stat"




   def do_mail(self, arg, opts=None):
       """Mail request"""
       sys.stdout.write(bcolors.TXT + "## Searching IP source...")
       sys.stdout.flush()
       con = []
       mailpkts = []
       for i, packet in enumerate(self.pcap):
           if TCP in packet:
               if packet.getlayer('TCP').dport == 110 or packet.getlayer('TCP').sport == 110 or packet.getlayer('TCP').dport == 143 or packet.getlayer('TCP').sport == 143:
                   if packet.getlayer('TCP').flags == 2:
                       con.append(i)
                   mailpkts.append(packet)
       sys.stdout.write("OK.\n")
       sys.stdout.flush()
       self.cmd = "mail"
       self.last = res

   def do_ipsrc(self, arg, opts=None):
       """Print the number of ip source and store its"""
       sys.stdout.write(bcolors.TXT + "## Searching IP source")
       sys.stdout.flush()
       ips = []
       for packet in self.pcap:
           if TCP in packet:
               if packet.getlayer('TCP').flag ==2:
                   res = packet.getlayer('IP').src
                   test = 0
                   for ip in ips:
                       ips.append(res)
                       sys.stdout.write(".")
                       sys.stdout.flush()
       sys.stdout.write("OK.\n")
       print bcolors.TXT + "Results : " + str(len(ips)) + " ips##" + bcolors.ENDC
       self.cmd = "ipsrc"
       self.last = ips

   def do_web(self, arg, opts=None):
       """Number web request"""
       sys.stdout.write(bcolors.TXT + "## Searching web's request....")
       sys.stdout.flush()
       con = []
       webpkts = []
       for i, packet in enumerate(self.pcap):
           if TCP in packet:
               if packet.getlayer('TCP').dport == 80:
                   if packet.getlayer('TCP').flags == 2:
                       con.append(i)
                       sys.stdout.write(".")
                       sys.stdout.flush()

                   webpkts.append(packet)
       sys.stdout.write("Ok.\n")
       print "\nWeb's request: " + str(len(con)) + bcolors.ENDC

       res = ""
       for packet inb webpkts:
           if packet.getlayer('TCP').flags == 24:
               res = res + packet.getlayer('Raw').load
       self.cmd = "web"
       self.last = res

   def do_followtcpstream(self, arg, opts=None):
       """Follow TCP sequence"""
       sys.stdout.write(bcolors.TXT + "## Searching TCP stream in PCAP...")
       sys.stdout.flush()
       l = self.pcap[int(arg)]
       ipsrc = l.getlayer("IP").src
       ipdst = l.getlayer("IP").dst
       portsrc = l.getlayer("TCP").sport
       portdst = l.getlayer("TCP").dport

       pkt = []
       pkt.append([])
       for i, p in enumerate(self.pcap):
           if p.haslayer('TCP'):
               if p[IP].src == ipsrc and p[IP].dst == ipdst and p[TCP].sport == portsrc and p[TCP].dport == portdst:
                   pkt.append([i, p])
               if p[IP].src == ipdst and p[IP].dst == ipsrc and p[TCP].sport == portdst and p[TCP].dport == portsrc:
                   pkt.append([i, p])
       sys.stdout.write("OK\n" + bcolors.ENDC)
       self.cmd = "followTCPStream"
       self.last = pkt

   def do_search(self, arg, opts=None):
       pkts = []
       pkts.append([])
       parser = OptionParser()
       parser.add_option("-p", "--protocol", dest="protocol", default="TCP", type="string", help="filtering by protocol")
       parser.add_option("--dport", "--destination-port", dest="dport", type="int", help="filtering by destination port")
       parser.add_option("--sport", "--source-port", dest="sport", type="int", help="filtering by source port")
       parser.add_option("--ipsrc", "--ip-source", dest="ipsrc", type="string", help="filtering by ip source")
       parser.add_option("--ipdst", "--ip-destination", dest="ipdst", type="string", help="filtering by ip destination")
       parser.add_option("-s", "--string", dest="stringdata", type="string", help="filtering by string")
       (options, args) = parser.parse_args(args=search)
       searchstring = ""
       nb = 1

       ## Create the request
       if options.protocol != None:
           if nb >1:
               searchstring = searchstring + ' and '
           searchstring = searchstring + '(packet.getlayer(\'' + options.protocol + '\') != None)'
           nb = nb + 1
       if options.dport != None:
           if nb > 1:
               searchstring = searchstring + ' and '
           searchstring = searchstring + '(packet.getlayer(\'' + options.protocol + '\').dport == ' + str(options.dport) + ')'
           nb = nb + 1
       if options.sport != None:
		  if nb > 1:
			   searchstring = searchstring + ' and '
		  searchstring = searchstring + '(packet.getlayer(\'' + options.protocol + '\').sport == ' + str(options.sport) + ')'
		  nb = nb + 1
	   if options.ipsrc != None:
			if nb > 1:
				searchstring = searchstring + ' and '
			searchstring = searchstring + '(packet.getlayer(\'IP\').src == "' + str(options.ipsrc) + '")'
			nb = nb + 1
	   if options.ipdst != None:
			if nb > 1:
				searchstring = searchstring + ' and '
			searchstring = searchstring + '(packet.getlayer(\'IP\').dst == "' + str(options.ipdst) + '")'
			nb = nb + 1
       if options.stringdata != None:
           if nb > 1:
               searchstring = searchstring + ' and '
           searchstring = searchstring + ' re.search("' + str(options.stringdata) + '", packet.getlayer(\'Raw\').load)'
           nb = nb + 1
       sys.stdout.write(bcolors.TXT + "## Sending request...")
       sys.stdout.flush()
       for i, packet in enumerate(self.pcap):
           try:
               if eval(searchstring):
                   pkts.append([i, packet])
                   sys.stdout.write(".")
                   sys.stdout.flush()
           except:
               error = ''
       print "\nSearch's result : " + str(len(pkts) -1)
       self.cmd = "search"
       self.last = pkts

   def do_show(self, arg, opts=None):
       args = arg.split(' ')
       if len(arg) < 1:
           if self.pcap != self.last:
               for var in self.last:
                   if self.cmd == 'ipsrc':
                       print var
                   elif (len(var)) == 2:
                       if self.cmd == "search" or self.cmd == "followTCPStream":
                           print(str(var[0]) + " | " + str(self.pcap[int(var[0])].summary()))
                       else:
                           print(str(var[0]) + " | " + str(var[1]))
                   elif (len(var)) == 1:
                       sys.stdout.write(str(var))
           elif len(args) == 1:
               if args[0] == "raw":
                   for p in self.last:
                       if len(p) > 0:
                           if self.pcap[int(p[0])].getlayer('Raw'):
                               print str(self.pcap[int(p[0])].getlayer('Raw').load)


               if args[0] == "pcap":
                   for i, p in enumerate(self.pcap):
                       print str(i) + " | " + str(p.summary())
               else:
                   self.pcap[int(arg)].show()

def main():
    shell = Forensic(sys.argv[1])
    shell.cmdloop()

if __name__ == '__main__':
    main() 
