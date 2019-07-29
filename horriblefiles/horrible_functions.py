# This file basically has all the functions and dictionaries that allow our system to be modular
# Which functions / variables are used depends on the user's preference settings

# add horriblehome to sys.path
import sys
import os
sys.path.append(os.path.expandvars('%horriblehome%'))

from collections import defaultdict as dd
from selenium import webdriver as wbd
from time import sleep
import pyautogui as pog

# Dictionary of web drivers according to browser
drivers = {
    'firefox': wbd.Firefox,
    'chrome': wbd.Chrome
}


# Function for when magnet link is opened in utorrent
def utorrent_download(path):
    while True:
        if pog.getWindowsWithTitle('Add New Torrent'):
            break
        sleep(0.2)
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press('enter')
    pog.press('enter')
    # close torrent software so focus is switched to web driver again for next anime
    sleep(1)


# Function for when magnet link is opened in qbittorrent
def qbittorrent_download(path):
    while True:
        if pog.getWindowsWithTitle('Magnet Link'):
            break
        sleep(0.2)
    pog.press(['\t', '\t', 'up', '\t', '\t'])
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    sleep(0.5)
    pog.press(['\t', '\t', '\t', '\t', '\t', '\t', '\t', '\t', '\t', '\t', 'space', 'enter'])
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
