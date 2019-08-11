# checks and downloads episodes of anime in the currently watching list

# add horriblehome to sys.path
import sys
import os

sys.path.append(os.path.expandvars('%horriblehome%'))

from horriblefiles.currently_watching import shows
import horriblefiles.horrible_functions as hf
from horriblefiles.user_preferences import preferences
from bs4 import BeautifulSoup as bs
from requests import get
import ctypes
from pyautogui import getWindowsWithTitle
from threading import Thread
from time import sleep

# read the contents of currently watching file
f = open(os.path.relpath(os.path.expandvars('%horriblehome%') + r'\horriblefiles\currently_watching.py', os.getcwd()),
         'r+')
cw = f.read()
f.close()

links = []

# iterate for each link
for i in shows.keys():

    print(i)  # print name of anime you are checking

    # var that stores which episode you are trying to download
    ep = str(shows[i])
    if len(ep) == 1:
        ep = '0' + ep

    ep_on_record = int(ep)

    # search on erai raws
    ep = hf.getCurrentEpisodes('Erai-raws', i, links, ep)

    # if nothing on erai raws, search on horrible
    if int(ep) == ep_on_record:
        ep = hf.getCurrentEpisodes('HorribleSubs', i, links, ep)

    # next time try to download the next episode by updating currently watching
    cw = cw.replace((i + '": ' + str(shows[i])), (i + '": ' + str(int(ep))))

    print('Up to date :)\n')

if len(links) != 0:
    i = -1


    def meow():  # function to thread - wait for 1 minute, then start check
        sleep(60)
        if i == -1:
            getWindowsWithTitle('horrible downloader')[0].close()


    t = Thread(target=meow)
    t.start()

    if ctypes.windll.user32.MessageBoxW(0, "Start downloading new episodes?", "horrible downloader", 0x1000) == 1:

        # startup procedure for torrent software
        hf.torrent_startup[preferences['torrent']]()

        for i in links:
            os.startfile(i['magnet'])
            hf.torrents[preferences['torrent']](i['path'])

            # close qbittorrent if open
            window = getWindowsWithTitle('qBittorrent')
            if len(window) > 0:
                for w in window:
                    w.close()

        # close μTorrent
        window = getWindowsWithTitle('μTorrent')
        if len(window) > 0:
            for w in window:
                w.close()

        # update the currently watching list
        f = open(
            os.path.relpath(os.path.expandvars('%horriblehome%') + r'\horriblefiles\currently_watching.py',
                            os.getcwd()),
            "w")
        f.write(cw)
        f.close()

        # Give the user time to read status report
        ctypes.windll.user32.MessageBoxW(0, "finished downloading all possible episodes :)", "horrible downloader",
                                         0x1000)  # popup
