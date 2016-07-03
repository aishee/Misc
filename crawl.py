import urllib2, cookielib
import urlparse
from BeautifulSoup import BeautifulSoup
import sqlite3
import time, datetime
import threading, Queue

time.clock() #initializing

globalData = {
    'userAgent': 'Crawler 0.0',
    'whiteList': [],
    'blackList': [],
        'startUrl': 'http://www.sony.co.jp/',
        'threadLimit': 1,
        'requestInterval': 0.5,
        'queue': [],
            'debug': True
}

class Crawl:
    def __init__(self):
        if globalData['debug']:
            print('Crawl | init called ')
        self.cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        self.db = DBOps()
    def getURL(self):
        if globalData['debug']:
            print('Crawl | getUrl called')
            #check for start URL
        if globalData['startURL']:
            url = [(0, globalData['startURL'])]
            globalData['startURL'] = None
        else:
            url = self.db.getURLFromQueue(globalData['threadLimit'])
        return url

    def requestURL(self, data):
      if globalData['debug']:
        print('Crawl | requestURL called')
        url = data['full_url']
        request = urllib2.Request(url)
        self.cookie.add_cookie_header(request)
        visitedtime = datetime.datetime.utcnow()
        try:
            start = time.clock()
            response = urllib2.urlopen(request)
            response = response.read()
            end = time.clock()
            loadtime = end - start
        except (urllib2.HTTPError, urllib2.URLError), e:
            response = None
            data.upgrade({'error': e})
            loadtime = 0
        data.update({'source' : response, 'loadtime': loadtime, 'request_url': url, 'visitedtime': visitedtime})
        return data
class DBOps:
    def __int__(self):
        if globalData['debug']:
            print('DBOps | init called')
        self.connection = sqlite3.connect('crawl.db')
        self.c = self.connection.cursor()
    def create(self):
        start = time.clock()
        if globalData['debug']:
            print(' DBOps | create called')
        self.c.execute('CREATE TABLE IF NOT EXISTS queue (url_id INTEGER PRIMARY KEY, url VARCHAR(1024))')
        self.c.execute('CREATE TABLE IF NOT EXISTS url_canonical (url_id INTEGER PRIMARY KEY, url VARCHAR(1024), times_visited INTEGER, times_referenced INTEGER)')
        self.c.execute('CREATE TABLE IF NOT EXISTS page_rel (link_src INTEGER, link_dest INTEGER, visit_id INTEGER)')
        self.c.execute('CREATE TABLE IF NOT EXISTS visit_metadata (visit_id INTEGER PRIMARY KEY, visited DATETIME, full_url VARCHAR(1024), scheme VARCHAR(64), netloc VARCHAR(256), path VARCHAR(256), params VARCHAR(256), query VARCHAR(256), fragment VARCHAR(256), \
            size INTEGER, loadtime FLOAT, num_links INTEGER, links_internal INTEGER, links_external INTEGER, error VARCHAR(512))')
        self.c.execute('CREATE INDEX IF NOT EXISTS idx_queue ON queue (url)')
        self.c.execute('CREATE INDEX IF NOT EXISTS idx_url_canonical ON url_canonical (url)')
        self.c.execute('CREATE INDEX IF NOT EXISTS idx_url_canonical_digits ON url_canonical (times_visited, times_referenced)')
        self.c.execute('CREATE INDEX IF NOT EXISTS idx_visit_metadata ON visit_metadata (full_url)')
        self.connection.commit()
        end = time.clock()
        if globalData['debug']:
            print(' DBOps | create completed in ', end - start)
        def getURLFromQueue(self, limit):
            start = time.clock()
            if globalData['debug']:
                print('DBOps | getURLFromQueue called')
            self.c.execute('SELECT * FROM queue LIMIT ? ', [str(limit)])
            end = time.clock()
            if globalData['debug']:
                print('DBOps | getURLFromQueue completed in', end - start)
                return self.c.fetchall()
            
        def updateCanonical(self, data):
            start = time.clock()
            if globalData['debug']:
                print('DBOps | update Canonical called')
                
        
