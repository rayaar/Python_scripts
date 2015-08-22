#!/bin/sh
 
# -q quiet
# -c nb of pings to perform
 
ping -q -c5 -W 3  google.com > /dev/null
 
if [ !  $? -eq 0 ]
then
	P=$(sudo nmcli -p con status | grep PIA | awk  '{ print $4 }')
	if [ -n "$P"  ]
	then
	sudo nmcli con down uuid $P
	fi
fi
