#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rr.py
#  downloads radioresepsjonen podcasts without Itunes
#  


import wget
import feedparser
import os
def main():
	print "downloading feed"
	feedURL = "http://podkast.nrk.no/program/radioresepsjonen.rss"
	print "parsing feed"
	feed = feedparser.parse(feedURL,agent='Internet Explorer v 2.0') 
	
	print "starting downloads"
	for item in feed.entries:
		link = item.links[0].href
		link=link[:(len(link)-17)]
		name= link[43:]
		#item.links[0].href=link
		
		if not os.path.isfile(str(name)):
			print "downloading ", link
			wget.download(link)
			print "\n"
		else:
			print "file", name, "already downloaded"
		
	print "done"
	
	return 0

if __name__ == '__main__':
	main()

