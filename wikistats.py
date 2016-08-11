#!/usr/bin/env python3

import sys
import urllib.request
import urllib.parse
import re
import os
import getopt
import datetime
from collections import OrderedDict

def usage():
    print('''\
Usage:
    python wikistats.py [options] <page_name>
        Get wikipedia article daily page views

    [options]:
        -h
        --help
            print this usage
        -l <language>
        --language=<language>
            wikipedia project language. default is en
        --startyear=<year>
        --startmonth=<month>
        --endyear=<year>
        --endmonth=<month>
    ''')

try:
    options, args = getopt.getopt(sys.argv[1:],
            "hl:", ["help", "language=", "startyear=", "startmonth=", "endyear=", "endmonth="])
except getopt.GetoptError:
    sys.exit()

startyear = None
startmonth = None
endyear = None
endmonth = None
language = None
for name, value in options:
    if name in ("-h", "--help"):
        usage()
        sys.exit()
    elif name in ("-l", "--language"):
        language = value
    elif name in ("--startyear"):
        startyear = int(value)
    elif name in ("--startmonth"):
        startmonth = int(value)
    elif name in ("--endyear"):
        endyear = int(value)
    elif name in ("--endmonth"):
        endmonth = int(value)
    else:
        usage()
        sys.exit()

# if len(args) < 1:
if len(args) != 1:
        usage()
        sys.exit()

article = args[0]

base_url = 'http://stats.grok.se'

language = 'en'
if not startyear:
    startyear = 2007
if not startmonth:
    startmonth = 12

year = startyear
month = startmonth

result = []

today = datetime.datetime.today()
curyear = today.year
curmonth = today.month
if not endyear:
    endyear = curyear
if not endmonth:
    endmonth = curmonth

while(True):
    if year > endyear:
        break
    if year == endyear and month > endmonth:
        break

    mon = str(month) if month > 9 else '0' + str(month)
    yearmonth = str(year) + mon
    url = base_url + '/' + language + '/' + yearmonth + '/' + urllib.parse.quote(article)

    print(url)

    res = urllib.request.urlopen(url).read().decode()

    m = re.search('line1 = \[\[.*?\]\]', res)
    data = [(i[0][0:-6], i[1]) for i in sorted(eval(res[m.start()+8:m.end()]))]

    print(data)
    result.extend(data)

    month = month + 1
    if month > 12:
        year = year + 1
        month = month % 12

print(OrderedDict(result))
