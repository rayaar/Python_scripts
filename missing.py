#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  findDupes.py
#  
#  Copyright 2015 raymond 

import os
import re
import time
import guessit
from operator import itemgetter
from pytvdbapi import api
import itertools
import time
import sys
from pytvdbapi import api
import subprocess
import datetime


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


def find_maks(name,seasonNum):
    db = api.TVDB('E86DDC318FFEA5D9', ignore_case=True)
    result = db.search(name, "en")
    if len(result) > 0:
        show = result[0]
    else:
        return -1
    if name.upper() == "Once Upon A Time".upper():
        for shows in result:
            if "2011" in shows.SeriesName:
                show = shows
            else:
                continue
    if name.upper() == "Archer".upper():
        for shows in result:
            if "2009" in shows.SeriesName:
                show = shows
            else:
                continue
    if name.upper() == "Legends".upper():
        for shows in result:
            if "2014" in shows.SeriesName:
                show = shows
            else:
                continue
    if name.upper() == "House of cards".upper():
        show = result[1]
    if len(show) >= seasonNum:
        season = show[seasonNum]
    else:
        return -1
    for i in range(len(season)):
        epiNumber = len(season)-i
        lastEP = season[epiNumber]
        lastEPDate = lastEP.FirstAired
        if isinstance(lastEPDate, datetime.date):
            today = datetime.datetime.today().date()
        else:
            return -1
        if today > lastEPDate:
            #print "found date for ",name,season," : ", lastEPDate,lastEP.EpisodeName,epiNumber
            return epiNumber

    print "should never happen"
    return -1


def remove_dupes(numbers, season):
    icount = {}
    for i in numbers:
        icount[i] = icount.get(i, 0) + 1
    for el in icount:
        if icount[el] > 1:
            delete = icount[el]-1
            for episode in season:
                if delete > 0:
                    if episode[2] == el:
                        print "removed duplicate: ", episode[3]
                        os.remove(episode[3])
                        delete=delete-1

def findMissingNumber3(array1, array2):

    missing = []
    for number in array1:
        if number not in array2:
            missing.append(number)
    return missing

def sizeof_fmt(num, suffix='B'):
    """
    returns a bytenumber to human readable
    :param num: number to convert to human readable
    :param suffix: soffix to calulate to. Bytes as standard
    :return: human readable size
    """

    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def getLength(filename):
    """ find playtime of vide """
    try:
        p1 = subprocess.Popen(["mplayer", "-vo", "dummy", "-ao", "dummy", "-identify",str(filename).encode('utf-8')],
            stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        p2 = subprocess.Popen(["grep", "ID_LENGTH"], stdin=p1.stdout, stdout = subprocess.PIPE)
        p1.stdout.close()
        result = p2.communicate()[0]
        p1.wait()
        return int(float(result.split("=")[1].strip()))
    except Exception as e:
        print e
        return 0
def rename(filename):

    words = filename
    match = re.search('S\d\dE\d\d', words)
    if match:
        m=  match.group()
        n = int(m[-2:])
        n = "%02d-E%02d" % (n,n+1)
        p = re.compile('S\d\dE\d\d')
        epp= m[0:-2]
        newname = p.subn( epp+n, words)[0]
        newname = newname
        #print "renaming to :", newname
        os.rename(filename,newname)


def missingLogic(season,missing):
    """Try to find double episodes of series. Used to go by filesize, now go by playtime"""
    for i,episode in enumerate(season,1):
        try:
            if (episode[2]+1) in missing:
                ep1 = episode
                ep2 = season[i]

                len1 = getLength(ep1[3])/60
                len2 = getLength(ep2[3])/60
                #calculate +-10% length of series
                min = int((len1*2) - ((15 * len1) / 100.0))
                max = int((len1*2) + ((15 * len1) / 100.0))
                min2 = int((len2*2) - ((15 * len2) / 100.0))
                max2 = int((len2*2) + ((15 * len2) / 100.0))

                #if "QI" in episode[0]:


                if min2 <= len1 <= max2:
                    missing.remove(episode[2]+1)
                    rename(episode[3])
                elif min <= len2 <= max:
                    #print episode
                    #print season[i-1][2]
                    missing.remove(season[i-1][2])
                    rename(season[i-1][2])

        except Exception as e:
            print e
            continue
    return missing


def logic(season,maks):
    #print "working on: ", season[0][0],"season",season[0][1]
    actual = []
    matching = [s for s in season if 0 in s] # check if there is a 0 episode in the season on server
    nums = [x + 1 for x in range(maks)]
    if len(matching) > 0:
        nums.insert(0,0)


    for episode in season:
        actual.append(episode[2])

    remove_dupes(actual,season)
    missing = findMissingNumber3(nums,actual)
    missing2 = []
    if (len(missing) > 0):
        missing = missingLogic(season,missing)
        if len(missing) > 0:
            #print season[0][0],"Season",season[0][1]
            #print missing+missing2
            return missing
    else:
        return []



def find_dupes_and_missing():
    #print "working on: ", season[0][0],"season",season[0][1]

    lowignore = ["moomi","adventure time with finn and jake","Adventure Time","HJØRDIS"]
    ignore = []
    for word in lowignore:
        ignore.append(word.upper())




    all_missing = []
    extensionsToCheck = ("mkv", "mp4", "avi")
    missing = []
    #print("iterating files")
    #print "Finding missing episodes and removing duplicates"


    #go through all files and folders:
    for root, dirs, files in os.walk('/media/server/serier'):
        missing = []
        if "season".upper() in root.upper():
            #print root
            season = []
            for fname in files:
                if str(fname).endswith(extensionsToCheck):
                    guess = guessit.guess_episode_info(fname)

                    if "episodeNumber" in guess and str(guess['series']).upper() not in ignore:
                        episode = [guess['series'], guess["season"], guess["episodeNumber"], os.path.join(root, fname)]
                        season.append(episode)

                        if "episodeList" in guess:
                            for number in guess['episodeList']:
                                if number != guess["episodeNumber"]:
                                    newEpisode = list(episode)
                                    newEpisode[2] = number
                                    #print newEpisode
                                    season.append(newEpisode)


            if len(season) > 0:
                season = sorted(season, key=itemgetter(2))
                try:
                    if len(season) > 1:
                        #
                        maks = season[-1][2] # find number of episodes in a folder
                        if ("Friends" in season[0][0] and season[0][1] == 8):
                            time.sleep(1)
                        actualMaks = find_maks(str(season[0][0]),season[0][1])
                        if actualMaks == -1:
                            actualMaks = maks
                    else:
                        print "Empty folder: " + root
                except Exception as e:
                            print e

                if (len(season) != maks):
                    missing = logic(season,maks)
                if maks != actualMaks:
                    for i in range(maks+1,actualMaks+1):
                        missing.append(i)
            if len(missing) > 0:
                print season[0][0],"Season",season[0][1]
                for miss in missing:
                    print miss,
                print


def main():
    global done
    try:
        find_dupes_and_missing()
    except KeyboardInterrupt:
        print "############   got controll + c, exiting   ############"
        sys.exit(1)
    #except Exception as e:
    #    print "Unexpected error:", e
    #    #time.sleep(2)
    #    sys.exit(1)
    return 0


if __name__ == '__main__':
    main()
