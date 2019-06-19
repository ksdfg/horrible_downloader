# This file basically has all the functions and dictionaries that allow our system to be modular
# Which functions / variables are used depends on the user's preference settings

from collections import defaultdict as dd
from selenium import webdriver as wbd
from time import sleep
import pyautogui as pog
import os

# Dictionary of web drivers according to browser
drivers = {
    'firefox': wbd.Firefox,
    'chrome': wbd.Chrome
}


# Function for when magnet link is opened in utorrent
def utorrent_download(path):
    sleep(3)
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press('enter')
    pog.press('enter')
    # close torrent software so focus is switched to web driver again for next anime
    pog.hotkey('alt', 'f4')
    sleep(2)


# Function for when magnet link is opened in qbittorrent
def qbittorrent_download(path):
    sleep(3)
    pog.press(['\t', '\t', 'up', '\t', '\t'])
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press(['\t', '\t', '\t', '\t', '\t', '\t', '\t', '\t', '\t', '\t', 'space', 'enter'])
    sleep(2)


# dictionary to decide which function should be called to start torrent download
torrents = {
    'utorrent': utorrent_download,
    'qbittorrent': qbittorrent_download
}

# dictionary that stores urls that download respective web driver and names of web drivers
download_driver = {
    'firefox': ['https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win',
                'geckodriver'],
    'chrome': ['https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_win32', 'chromedriver']
}


# function to startup qbittorrent in the beginning
def qbittorrent_startup():
    os.startfile(r"C:\Program Files\qBittorrent\qbittorrent.exe")
    sleep(5)
    pog.hotkey('alt', 'f4')


# default dictionary that returns the startup functions of torrenting softwares
torrent_startup = dd(lambda: lambda: None)
torrent_startup['qbittorrent'] = qbittorrent_startup
