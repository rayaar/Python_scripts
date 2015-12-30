#!/home/raymond/missing/bin/python
# -*- coding: utf-8 -*-
#
#  findDupes.py
#  
#  Copyright 2015 raymond 

import os
import re
import itertools
import threading
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
import pickle

done = False
def animate():
    global done
    for c in itertools.cycle(['-', '/', '|', '\\']):
        if done:
            sys.stdout.flush()
            time.sleep(.5)
            sys.stdout.flush()
            break
        sys.stdout.write('\rFinding missing episodes and removing duplicates |' + c + "|")
        sys.stdout.flush()
        time.sleep(.5)
    #sys.stdout.write('\rDone!     ')


def find_maks(name,seasonNum):
    db = api.TVDB('TVDB_API_KEY', ignore_case=True)
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
    dupes = []
    for i in numbers:
        icount[i] = icount.get(i, 0) + 1
    for el in icount:
        if icount[el] > 1:
            delete = icount[el]-1
            for episode in season:
                if delete > 0:
                    if episode[2] == el:
                        dupes.append(episode[3])
                        os.remove(episode[3])
                        delete=delete-1
    return dupes
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
        return filename+ " : "+ newname
    return ""


def missingLogic(season,missing):
    """Try to find double episodes of series. Used to go by filesize, now go by playtime"""
    newName = []
    for i,episode in enumerate(season,1):
        try:
            if i <= len(season):
                if (episode[2]+1) in missing and i != len(season):
                    ep1 = episode
                    ep2 = season[i]

                    len1 = getLength(ep1[3])/60
                    len2 = getLength(ep2[3])/60

                    min = int((len1*2) - ((15 * len1) / 100.0))
                    max = int((len1*2) + ((15 * len1) / 100.0))
                    min2 = int((len2*2) - ((15 * len2) / 100.0))
                    max2 = int((len2*2) + ((15 * len2) / 100.0))

                    if min2 <= len1 <= max2:
                        missing.remove(episode[2]+1)
                        new = rename(episode[3])
                        if new != "":
                            newName.append(new)
                    elif min <= len2 <= max:
                        #print episode
                        #print season[i-1][2]
                        missing.remove(episode[2]+1)
                        new = rename(episode[3])
                        if new != "":
                            newName.append(new)
                elif (episode[2]+1) in missing and i == len(season):
                    ep1 = episode
                    ep2 = season[i-2]

                    len1 = getLength(ep1[3])/60
                    len2 = getLength(ep2[3])/60

                    min = int((len1*2) - ((15 * len1) / 100.0))
                    max = int((len1*2) + ((15 * len1) / 100.0))
                    min2 = int((len2*2) - ((15 * len2) / 100.0))
                    max2 = int((len2*2) + ((15 * len2) / 100.0))

                    if min2 <= len1 <= max2:
                        missing.remove(episode[2]+1)
                        new = rename(episode[3])
                        if new != "":
                            newName.append(new)
        except Exception as e:
            print e
            continue
    return missing,newName


def logic(season,maks):
    name =  str(season[0][0])+" season "+ str(season[0][1])
    newName = []
    #print "working on: ", name
    actual = []
    matching = [s for s in season if 0 in s] # check if there is a 0 episode in the season on server
    nums = [x + 1 for x in range(maks)]
    if len(matching) > 0:
        nums.insert(0,0)


    for episode in season:
        actual.append(episode[2])

    dupes = remove_dupes(actual,season)
    missing = findMissingNumber3(nums,actual)
    if (len(missing) > 0):
        missing,newName = missingLogic(season,missing)

    return missing,dupes,newName

def saveFile(missing):
    with open('/home/raymond/missing/missing.save', 'wb') as f:
        pickle.dump(missing,f)

def find_dupes_and_missing():
    lowignore = ["moomi","adventure time with finn and jake","Adventure Time","HJØRDIS"]
    ignore = []
    newName = ""
    for word in lowignore:
        ignore.append(word.upper())

    all_missing = []
    dupes = []
    extensionsToCheck = ("mkv", "mp4", "avi")
    missing = []

    #print "Finding missing episodes and removing duplicates"
    t = threading.Thread(target=animate)
    t.start()

    #go through all files and folders:
    for root, dirs, files in os.walk('PATH/TO/SERIES'):
        missing = []
        newName = []
        if "SEASON" in root.upper():
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
                        maks = find_maks(str(season[0][0]),season[0][1])#season[-1][2] # find number of episodes in a folder
                        actualMaks = find_maks(str(season[0][0]),season[0][1])
                        if actualMaks == -1:
                            actualMaks = maks

                except Exception as e:
                            print e
                if maks != actualMaks:
                    missing,dupes,newName = logic(season,maks)
                    for i in range(maks+1,actualMaks+1):
                        missing.append(i)
                if (len(season) != maks):
                    missing,dupes,newName = logic(season,maks)

            if len(missing) > 0:
                sname = season[0][0]+" S%02d" % (season[0][1])
                all_missing.append([sname,missing])
    global done
    done = True
    time.sleep(1)
    print

    if len(dupes) > 0:
        print "Found duplicated episode(s): "
        for ep in dupes:
            print "removed ",ep
    if len(newName) > 0:
        print "Found double episode(s): "
        for ep in newName:
            oldnew = ep.split(":")
            print "Rewrote ", oldnew[0]
    if len(all_missing) > 0:
        print "Found missing episodes: "
        for liste in all_missing:
            print liste[0]
            for number in liste[1]:
                print number,
            print
        saveFile(all_missing)
        print "Trying to download missing episodes"
        os.system("/path/to/torrent.py")
    else:
        print "No missing episodes found :)"


def main():
    global done
    try:
        find_dupes_and_missing()
    except KeyboardInterrupt:
        global done
        done = True
        time.sleep(1)
        print
        print "############   got controll + c, exiting   ############"
        sys.exit(1)
    except Exception as e:
        print "Unexpected error:", e
        #time.sleep(2)
        sys.exit(1)
    return 0


if __name__ == '__main__':
    main()
