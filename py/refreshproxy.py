#!/bin/env python
#-*- coding:utf-8 -*-
from BeautifulSoup import *
import libxml2
import urllib2, httplib
import urllib
import sys
import traceback
import os
import csv
import md5
import re
import random
import StringIO

url = "http://www.5udaili.com/http_non_anonymous.html"
url = "http://www.5udaili.com/http_anonymous.html"
headers = [
        ('Host',   'www.5udaili.com'),
        ('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'zh-cn,en-us;q=0.7,en;q=0.3'),
        ('Accept-Encoding', 'deflate'),
        ('Accept-Charset', 'utf-8;q=0.7,*;q=0.7'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Referer', 'http://www.5udaili.com')]

opener = urllib2.build_opener()
urllib2.install_opener(opener)
opener.addHeaders = headers
req = urllib2.Request(url)
f = urllib2.urlopen(req)

z = f.read(4096)
buf = ''
while z:
    buf += z
    z = f.read(4096)

content = buf.decode('utf-8')
urls = []
soup = BeautifulSoup(content)
lists = soup.findAll("div", {"id": "tb"})
newhosts = []
for item in lists:
    trs = item.findAll("tr")
    for tr in trs:
        tds = tr.findAll("td")
        _idx = 0
        ip = ''
        port = ''
        cn = ''
        for td in tds:
            if _idx == 1:
                ip = td.string
            if _idx == 2:
                port = td.string
            if _idx == 3:
                cn = td.string
            _idx += 1
#        if cn.lower() == 'cn':
        newhosts.append("\"" + str(ip) + ":"  +  str(port) + "\",")
        

f = open('/root/fineinfo/proxy.py', 'w')
print >> f, '''
#!/bin/env python
#-*- coding:utf-8 -*-
proxys = [ '''
for host in newhosts:
    print >> f, host.strip()
print >> f, "]"

