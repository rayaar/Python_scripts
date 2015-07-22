#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A small script to get the name of your location based on IP 
#  


import requests
import time;
def main():
	locate()
	


def locateCountry():
	try:
		country = ""
		ip = requests.get("http://icanhazip.com",timeout=1)
		key = "Key"
		url="http://api.ipinfodb.com/v3/ip-country/?key="+key+"&ip="+ip.text
		r = requests.get(url,timeout=2)
		req = r.text.split(";")
		country = req[4].lower()
	except :
		locate()
		pass
	return country



def locate():
	try:
		country = ""
		ip = requests.get("http://icanhazip.com",timeout=1)
		url="http://api.ipinfodb.com/v3/ip-city/?key=22446a5de0a0521b7f1c057744cbc1b3a1d4f9a36f5e8d507a3d466ba0dd6609&ip="+ip.text
		r = requests.get(url,timeout=2)
		req = r.text.split(";")
		country = req[4].lower()
		city = req[6].lower()
		print city +","+  country
	except :
		locate()
		pass
	return country

if __name__ == '__main__':
	main()

