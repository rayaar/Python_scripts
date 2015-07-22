#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 raymond <raymond@skole-crunch>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


"""
Get all vpn connections registered on this computer.
Password needed manually if not remembered! 
"""
import commands, os, threading, urllib2
from random import choice



def get_uiid():
	uuids = []
	status, output = commands.getstatusoutput("nmcli -p -m multiline con")
	k = output.split("\n")
	k=k[3:]
	name = ""
	
	for i in range(len(k)-1):
		p = k[i].split()
		q = k[i+1].split()
		if "NAME" in p[0] and "PIA" in p:
			if len(p)>4:
				name =' '.join(p[len(p)-2:])
			else:
				name= str(p[len(p)-1:])
			uuids.append(q[1])
	print  uuids
	return uuids

def main():
	uuids = {}
	status, output = commands.getstatusoutput("nmcli -p -m multiline con")
	k = output.split("\n")
	k=k[3:]
	name = ""
	names = {}
	
	for i in range(len(k)-1):
		p = k[i].split()
		q = k[i+1].split()
		if "NAME" in p[0] and "Wired" not in p and "PIA" in p:
			if len(p)>4:
				name =' '.join(p[len(p)-2:])
			else:
				name= str(p[len(p)-1:])
			names[name]=q[1]
	for item in names.keys():
		print item
		print names[item]
	return 0

if __name__ == '__main__':
	get_uiid()

