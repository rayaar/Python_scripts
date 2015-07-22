#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pianoping.py
#  
#  Copyright 2015 raymond <raymond@skolePc>
#  
#  
#  A small script to download check if a proxy is up.
#  if proxy is down, get a new one that is working.
#  

from bs4 import BeautifulSoup
import requests
import nmap
from os.path import expanduser
import sys

def writeFile(IP):
	home = expanduser("~")
	infile = home + "/.config/pianobar/config"
	
	pqr = ""
	with open(infile) as f:
	    for line in f:
			if "control_proxy =" in line:
				if "0.0.0.0" in line:
					line = "#control_proxy = " + IP + "\n"
				else:
					line = "control_proxy = " + IP + "\n"
			pqr= pqr + line
	with open(infile, "w") as out:
		for line in pqr:
			out.writelines(line)
		out.writelines("\n")
			
def getIP(num=0):
	nm = nmap.PortScanner()
	r  = requests.get("http://www.us-proxy.org/")
	data = r.text
	soup = BeautifulSoup(data)
	rows = soup.find_all('tr')
	
	counter = 0
	for row in rows:
	    data2 = row.find_all("td")
	    if data2 != []:
		    ip = str(data2[0].get_text())
		    port = data2[1].get_text()
		    d = data2[2].get_text()
		    country = data2[3].get_text()
		    proxyType = data2[4].get_text()
		    if "elite" or "anonymous" in proxyType:
			    status = nm.scan(hosts=ip, arguments='-sn')
			    if ip in status["scan"] and status["scan"][ip]["status"]["state"] == "up":
					ip= ip+":"+port
					if counter >= 0:
						return "http://" + ip
					else:
						continue
	return "0.0.0.0"
	

def main(num=0):
	if num == "-1":
		print "writing 0000"
		writeFile("0.0.0.0")
	else:
		IP = getIP(num)
		writeFile(IP)
	return 0

if __name__ == '__main__':
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		main()

