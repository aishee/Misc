import urllib2
import threading
import Queue
import urllib
import sys

def credit():
    print "%sDirectory Bruteforce%s" % (yel, norm)

red = "\033[01;31m"
green = "\033[01;32m"
yel = "\033[01;33m"
norm = "\033[0m"

credit()
threads = 50
target_url = raw_input("Site: ")
wordlist_file = raw_input("Wordlist file: ")
resume = None
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0"

def build_wordlist(wordlist_file):
    fb = open(wordlist_file, "rb")
    raw_words = fb.readlines()
    fb.close()
    
    found_resume = False
    words = Queue.Queue()
    for word in raw_words:
        word=word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume
        else:
            words.put(word)
    return words

def dir_bruter(word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("%s/" % attempt)
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" %(attempt, extension))
            for brute in attempt_list:
                url = "%s%s" %(target_url, urllib.quote(brute))
                try:
                    headers = {}
                    headers["User-Agent"] = user_agent
                    r = urllib2.Request(url, headers=headers)
                    response = urllib2.urlopen(r)
                    if len(response.read()):
                        print "[%s%d%s] => %s" %(green, response.code, norm, url)
                except urllib2.HTTPError, e:
                    if hasattr(e, 'code') and e.code != 404:
                        pass
                except urllib2.URLError:
                    pass
if "http" not in target_url:
    target_url = "http://" + target_url
if target_url[-1] != "/":
    target_url += "/"

try:
    f = open(wordlist_file, "r")
    f.close()
except IOError:
    print "%sFile %s inesistente %s" %(red, wordlist_file, norm)
    sys.exit()

word_queue = build_wordlist(wordlist_file)
extensions = [".php",".bak", ".orig", ".inc"]
for i in range(threads):
    try:
        t = threading.Thread(target=dir_bruter, args=(word_queue, extensions,))
        t.start()
    except threading.ThreadError:
        continue