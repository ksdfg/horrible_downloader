# This file basically has all the functions and dictionaries that allow our system to be modular
# Which functions / variables are used depends on the user's preference settings

from collections import defaultdict as dd
from selenium import webdriver as wbd
from time import sleep
import pyautogui as pog
import requests
import os
import zipfile
import io

# Dictionary of web drivers according to browser
drivers = {
    'firefox': wbd.Firefox,
    'chrome': wbd.Chrome
}


# A function that returns the element which, when clicked, brings links of episode to be downloaded in view
def episode_selector(webdriver, ep, browser):
    if browser == 'firefox':
        return webdriver.find_element_by_css_selector(r'.rls-label')
    elif browser == 'chrome':
        return webdriver.find_element_by_xpath('//*[@id="' + ep + '"]/a')


# A funtion that returns the element which, when clicked, opens magnet link
def magnet_selector(webdriver, ep, quality, browser):
    if browser == 'firefox':
        return webdriver.find_element_by_css_selector(r'#\3' + ep[0] + ' ' + ep[1:] + '-' + quality + '> span:nth-child(2) > ''a:nth-child(1)')
    elif browser == 'chrome':
        return webdriver.find_element_by_xpath('//*[@id="' + ep + '-1080p"]/span[2]/a')


# dictionary to select what key presses are required to open torrent in downloading software
torrent_opener = {
    'firefox': ['\t', '\t', '\t', '\t', 'enter'],
    'chrome': ['left', 'enter']
}


# Function for when magnet link is opened in utorrent
def utorrent_download(path):
    sleep(3)
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press('enter')
    sleep(5)
    pog.press('enter')
    # close torrent software so focus is switched to web driver again for next anime
    sleep(1)
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


# function to download geckodriver during setup
def geckodriver_download():
    driver_path = os.path.join('C:', 'Users', os.getlogin(), 'AppData', 'Local', 'Programs', 'Python', 'Python37',
                               'Lib', 'site-packages', 'selenium', 'webdriver', 'firefox')
    print('Downloading web driver...')
    # download file from github
    win = '64' if 'PROGRAMFILES(X86)' in os.environ else '32'
    r = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win' + win +
                     '.zip', stream=True)
    print('Downloaded zip file from the internet.\nExtracting zip file...')
    r = zipfile.ZipFile(io.BytesIO(r.content))  # convert file to zip file
    r.extractall(driver_path)   # extract zip file at given path
    print('extracted zip file.')
    return driver_path + '\\geckodriver.exe'    # make driver path be path to driver.exe and return it


# dictionary that stores methods that download respective web driver
download_driver = {
    'firefox': geckodriver_download
}


# function to startup qbittorrent in the beginning
def qbittorrent_startup():
    os.startfile("C:\Program Files\qBittorrent\qbittorrent.exe")
    sleep(5)
    pog.hotkey('alt', 'f4')


# default dictionary that returns the startup functions of torrenting softwares
torrent_startup = dd(lambda: lambda: None)
torrent_startup['qbittorrent'] = qbittorrent_startup

