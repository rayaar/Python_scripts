#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  findDupes.py
#  
#  Copyright 2015 raymond 

import os
import time
import guessit
from operator import itemgetter
import requests
import itertools
import threading
import time
import sys

done = False

def animate():
    global done
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
			sys.stdout.flush()
			break
        sys.stdout.write('\rReading files ' + c)
        sys.stdout.flush()
        time.sleep(.5)
    #sys.stdout.write('\rDone!     ')






def get_id(name):
    tvname = name
    # tvname = "\""+tvname+"\""
    # time.sleep(5)
    r = requests.get('http://api.tvmaze.com/singlesearch/shows?q="' + tvname + "\"")
    r = r.json()
    tvdb = r["externals"]["thetvdb"]
    return tvdb

def find_dupes_and_missing():
	
	
    ignore = ["Series to ignore"]
    all_missing = []
    extensionsToCheck = ("mkv", "mp4", "avi")
    missing = []
    #print("iterating files")
    print "finding missing episodes and removing duplicates"    
    #make animation:
    #t = threading.Thread(target=animate)
    #t.start()
    
    #go through all files and folders:
    for root, dirs, files in os.walk('Folder with series. Absolute path'):
        series = []
			
		#iterate over files:
        for item in files:
            if str(item).endswith(extensionsToCheck) and "Extra" not in item:
                try:
					#find show info:
                    guess = guessit.guess_episode_info(item)
                    #id = get_id(guess['series'])
                    #episode = [guess['series'], guess["season"], guess["episodeNumber"], os.path.join(root, item),id]
                    episode = [guess['series'], guess["season"], guess["episodeNumber"], os.path.join(root, item)]

                    series.append(episode)
                except Exception as inst:
                    continue

        series = sorted(series, key=itemgetter(2))#sort by episode
        
        if len(series) == 1:
			continue #if only one episode, assume all episodes are there.
        
        #if more than one episode in folder
        if len(series) > 1:
            maks = series[-1][2] # find number of episodes in a folder
            try:
                nameAndSeason = str(series[-1][0].encode("utf8")), "season " + str(series[-1][1])#get name and season info

            except Exception as e:
                print "Error:", series[-1][0], " season ", series[-1][1]
            nums = [x + 1 for x in range(maks)]
            for i, serie in enumerate(series):
				if i >= 1:
					try:
						num1 = series[i - 1][2]
						num2 = serie[2]
						size1 = os.path.getsize(series[i - 1][3])
						size2 = os.path.getsize(serie[3])
						sizer = (size1*2)
						sizer2 = (size2*2)
					except Exception as e:
						continue

					sum1 = ((sizer >= size2 - ((25 * size2) / 100.0)) and (sizer <= size2+((35 * size2) / 100.0)))
					sum2 = ((sizer2 >= size1 - ((20 * size1) / 100.0)) and (sizer2 <= size1+((20 * size1) / 100.0)))
					
					
					#print sum1
					###special episode:####
					if num1 ==0:						
						continue
					#duplicate:
					if num1 == num2:
						print "removed duplicate: ", serie[3]
						os.remove(serie[3])
						continue
					#fjerne:
					if num1 in nums:
						nums.remove(num1)
					#double episode logic:
					if sum1 and num2 < maks:
						nums.remove(num2+1)
					if sum2 and num1 >= 1 and num1+1 in nums:
						nums.remove(num1+1)
					
					#if last element, remove it:
					if(num2 ==maks and num2 in nums):
						nums.remove(num2)
				
						

			#if there are missing episode, save to a list the name and season + what episodes are missing.
            if len(nums) > 0 and len(nameAndSeason) > 0 and (nameAndSeason[0] not in ignore):
                missing.append([nameAndSeason, nums])
    global done
    done = True
    sys.stdout.flush()
    
    #print missing episodes from the list:
    print "\n----------------------------------------------------"
    print "Missing episodes: \n"  
  
    for season in missing:
        print season[0][0],season[0][1]
        for episodes in season[1]:
            print episodes,

        print

def main():
	global done
	try:
		find_dupes_and_missing()
	except KeyboardInterrupt:
		print "############   got controll + c, exiting   ############"
		
		done = True
		time.sleep(2)
		sys.exit(1)
	"""except Exception as e:
		print "Unexpected error:", e
		done = True
		time.sleep(2)
		sys.exit(1)
        """
	return 0


if __name__ == '__main__':
    main()
