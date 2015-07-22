#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wait untill the computer has been idle for a certain amount of time,
#  and then login to google as them, and install an app on their phone.
#  A POC to help a friend on his Masters-thesis  

from selenium import webdriver
import time
from ctypes import Structure, windll, c_uint, sizeof, byref
 
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]
 
def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

while 1:
    GetLastInputInfo = int(get_idle_duration())
    if GetLastInputInfo == 300:
		fp = webdriver.FirefoxProfile('~/.mozilla/firefox/cdjlvolh.default')
		browser = webdriver.Firefox(fp)
		url = "https://play.google.com/store/apps/details?id=com.yahoo.mobile.client.android.yahoo"
		browser.get(url)
		browser.find_element_by_css_selector('button.price.buy').click()
		browser.find_element_by_css_selector('.play-button.apps.loonie-ok-button').click()
    time.sleep(1)

