#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pomodoro.py
#  
#  Copyright 2015 raymond <raymond@aarseth.me>
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
import sys
import easygui as g
import time
import socket
import httplib, urllib
import os

def push(message):
	host =(socket.gethostname())
	message = host+ ": " + message
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	urllib.urlencode({
    "token": "token",
    "user": "token",
    "message": message,
	}), { "Content-type": "application/x-www-form-urlencoded" })


def timer(sleepTime):
	startTime = time.time()
	finishTime = startTime + sleepTime
	
	cnt = 0
	while time.time() < finishTime:
		mins = (sleepTime-cnt)/60
		secs = (sleepTime-cnt)%60
		sys.stdout.write(str(mins)+ ":" + str(secs) + " left \r")
		sys.stdout.flush()
		cnt +=1
		
		time.sleep(1)
	return
	
	
def main():
	msg = "Start pomodoro-timing?"
	choices = ["Yes","No"]
	reply = g.buttonbox(msg, choices=choices)

	if reply == "Yes":
		title = "Please Confirm"
		print("25 minute work")
		timer(1500)
		choices = ["Yes","No","Long break!","Lunch"]
		while(True):
			#push("Pause")
			os.system('cls' if os.name == 'nt' else 'clear')
			reply = g.buttonbox("Worked for 25 min. Time for a break! \n Do you want to continue?" ,choices=choices)
			if reply == "Yes":
				print("5 min break")
				timer(300)
			elif reply == "Long break!":
				print("long break! coma back in 15 minutes!")
				timer(900)
			elif reply == "Lunch":
				print("Taking a 30 min lunch!")
				timer(1800)
			else:
				break
			
			push("Pause over! Get back to Work!")
			if g.ccbox("Five minute break over! Time to work the next 25 min! \n Do you want to continue?", title):
				print("sleeping for 25 minutes")
				timer(1500)
				#print(chr(27) + "[2J")
			else:  
				break
			
if __name__ == '__main__':
	try:
		os.system('cls' if os.name == 'nt' else 'clear')
		main()
	except KeyboardInterrupt:
		try:
			os.system('cls' if os.name == 'nt' else 'clear')
			print "Got ctrl+C, exiting :)"
			time.sleep(2)
			sys.exit()
		except KeyboardInterrupt:
			sys.exit()
