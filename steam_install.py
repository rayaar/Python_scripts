#!/usr/bin/env python
# -*- coding: utf-8 -*-


#"""script for automatic installation of steam on crunchbang """



import wget,sys,os, time
from pkg_resources import WorkingSet , DistributionNotFound
from setuptools.command.easy_install import main as install
def main():
	"""script for automatic installation of steam on crunchbang """
	working_set = WorkingSet()
	# Detecting if module is installed
	try:
	    dep = working_set.require('wget>=1.0')
	except DistributionNotFound:
		print "missing modules. need wget to work. Try 'easy_install wget'"
		
	is_64bits = sys.maxsize > 2**32
	steam="http://media.steampowered.com/client/installer/steam.deb"
	xkit="http://mirrors.us.kernel.org/ubuntu//pool/main/x/x-kit/python-xkit_0.4.2.3build1_all.deb"
	jockey="http://mirrors.us.kernel.org/ubuntu//pool/main/j/jockey/jockey-common_0.9.7-0ubuntu7_all.deb"
	
	steamf=wget.download(steam)
	print 
	xkitf=wget.download(xkit)
	print 
	jockeyf=wget.download(jockey)
	print 
	time.sleep(2)
	
	os.system("sudo dpkg --install " + xkitf)
	os.system("sudo dpkg --install " + jockeyf)

	if is_64bits:
		os.system("sudo dpkg --add-architecture i386")
	
	os.system('echo "##remove this and the line underneath:" | sudo tee -a /etc/apt/sources.list ')
	os.system('echo "deb http://ftp.de.debian.org/debian sid main" | sudo tee -a /etc/apt/sources.list ')
	os.system("sudo apt-get update")
	os.system("sudo apt-get install libc6")
	os.system("sudo dpkg --install " + steamf)
	os.system("steam &")
	os.system("sudo geany /etc/apt/sources.list")
	
	return 0



if __name__ == '__main__':
	main()
