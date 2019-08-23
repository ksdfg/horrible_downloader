# This file basically has all the functions and dictionaries that allow our system to be modular
# Which functions / variables are used depends on the user's preference settings

# add horriblehome to sys.path
import sys
import os

sys.path.append(os.path.expandvars('%horriblehome%'))

from collections import defaultdict as dd
from time import sleep
import pyautogui as pog
import requests
from bs4 import BeautifulSoup as bs
import re
from horriblefiles.user_preferences import preferences


# Function for when magnet link is opened in utorrent
def utorrent_download(path):
    while True:
        if pog.getWindowsWithTitle('Add New Torrent'):
            break
        sleep(0.2)
    pog.typewrite(path)  # enter path where you want to store the downloaded episode
    pog.press('enter')
    pog.press('enter')
    # close torrent software so focus is switched to web driver again for next anime
    sleep(1)


# Function for when magnet link is opened in qbittorrent
def qbittorrent_download(path):
    while True:
        if pog.getWindowsWithTitle('[HorribleSubs]'):
            break
        sleep(0.2)

    pog.press(['\t', '\t', '\t', '\t'])
    pog.typewrite(path)     # enter path where you want to store the downloaded episode

    sleep(0.5)
    pog.press(['\t', '\t', '\t', '\t', '\t', '\t', '\t', 'space', 'enter'])
    sleep(1)


# dictionary to decide which function should be called to start torrent download
torrents = {
    'utorrent': utorrent_download,
    'qbittorrent': qbittorrent_download
}


# function to startup qbittorrent in the beginning
def qbittorrent_startup():
    os.startfile(r"C:\Program Files\qBittorrent\qbittorrent.exe")
    while True:
        if pog.getWindowsWithTitle('qBittorrent'):
            pog.getWindowsWithTitle('qBittorrent')[0].close()
            break
        sleep(0.2)


# default dictionary that returns the startup functions of torrenting softwares
torrent_startup = dd(lambda: lambda: None)
torrent_startup['qbittorrent'] = qbittorrent_startup


def getEpisode(name, order):
    soup = bs(requests.get('https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') +
                           '+720p' + '&s=id&o=' + order).text, features='html.parser')
    # get name of first ep released
    ep = -1
    epNames = soup.select('tr.success > td:nth-child(2)')
    for epName in epNames:
        title = [i.text for i in epName.findChildren('a') if not i.findChild('i')][0]
        if re.findall('\[HorribleSubs\] ' + name + ' - \d+.* \[.+\]\.mkv', title):
            # get the ep number from that name
            ep = int(re.compile('\d+').findall(re.compile(' - \d+.* \[').findall(title)[0])[0])
            break
    return ep


def getCurrentEpisodes(site, show, links, ep):
    while True:
        soup = bs(requests.get(
            'https://nyaa.si/user/' + site + '?f=0&c=1_2&q=' + show.replace(' ', '+') + '+' + ep + '+' + preferences[
                'quality']).text, features='html.parser')
        link = [i.get('href') for i in soup.select('td[class="text-center"] > a') if
                'fa-magnet' in i.findChild('i').get('class')]
        if len(link) == 0:
            break

        # define path where episode is to be downloaded
        path = preferences['download_path'] + show
        if not os.path.exists(path):
            os.mkdir(path)  # if directory doesn't exist, make one

        links.append({'magnet': link[0], 'path': path})

        print("Queueing episode", ep, "for download :)")

        ep = str(int(ep) + 1)
        if len(ep) == 1:
            ep = '0' + ep

    return ep
