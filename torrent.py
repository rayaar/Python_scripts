#!/home/raymond/missing/bin/python
# -*- coding: utf-8 -*-
#
#  torrent.py
#
#  Copyright 2015 raymond

from bs4 import BeautifulSoup
import mechanize
from mechanize import ParseResponse, urlopen,urljoin
import re
import pickle
import time


def findEPNum(filename,expected):
    words = filename
    match = re.search('S\d\dE\d\d', words)
    if match and match.group() == expected:
        m=  match.group()
        return True
    return False


def find_torrent(br,query,se):
    rsp = br.open(url + "/torrents/browse/index/query/"+query+"/categories/26")
    soup = BeautifulSoup(rsp,'html.parser')
    dl = soup.find("table", {"id": "torrenttable"})
    for link in dl.find_all('a'):
        if link.get('href').endswith(".torrent"):
            dl = link.get('href')
            if ("SPANISH" not in dl.upper()) and ("HEBSUB" not in dl.upper()):
                if findEPNum(dl,se):
                    urldl= urljoin(url, dl)
                    fname = dl.split("/")[-1]
                    torrent = br.open(urldl).read()
                    file = open("/path/to/downloads/"+fname,"w")
                    file.write(torrent)
                    file.close()
                    break
                else:
                    continue


with open('/path/to/missing.save', 'rb') as f:
    missing = pickle.load(f)


if len(missing) >= 0:
    user= "UserName"
    passw = "password"
    url = "http://URL.org"

    br = mechanize.Browser()
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    br.addheaders = [('User-agent', 'Firefox')]

    response = br.open(url)
    forms = ParseResponse(response, backwards_compat=False)
    form = forms[0]
    form["username"] = user
    form["password"] = passw
    br.open(form.click())
    for liste in missing:
                fname = ' '.join(liste[0].split()[0:-1])
                seasonNumber = liste[0].split()[-1]
                for number in liste[1]:
                    expected = seasonNumber+"E%02d" % (number)
                    find_torrent(br,fname,expected)
                    time.sleep(1)
                    #print fname,expected
