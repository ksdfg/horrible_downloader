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
from selenium.common.exceptions import NoSuchElementException
from horriblefiles.user_preferences import preferences

# Dictionary of web drivers according to browser
drivers = {
    'firefox': wbd.Firefox,
    'chrome': wbd.Chrome
}

# Function for waiting until magnet link popup is Active for either Torrent Software
def wait_for_magnet():
    while True:
        if pog.getWindowsWithTitle('Magnet Link'):
            break;
        sleep(0.2)

# Function for when magnet link is opened in utorrent
def utorrent_download(path):
    wait_for_magnet()
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press('enter')
    pog.press('enter')
    # close torrent software so focus is switched to web driver again for next anime
    pog.hotkey('alt', 'f4')
    sleep(2)


# Function for when magnet link is opened in qbittorrent
def qbittorrent_download(path):
    wait_for_magnet()
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

# dictionary that stores urls that download respective web driver and names of web drivers
download_driver = {
    'firefox': ['https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-win',
                'geckodriver'],
    'chrome': ['https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_win32', 'chromedriver']
}


# function to startup qbittorrent in the beginning
def qbittorrent_startup():
    os.startfile(r"C:\Program Files\qBittorrent\qbittorrent.exe")
    while True:
        if pog.getWindowsWithTitle('qBittorrent'):
            pog.getWindowsWithTitle('qBittorrent')[0].close()
            break;
        sleep(0.2)


# default dictionary that returns the startup functions of torrenting softwares
torrent_startup = dd(lambda: lambda: None)
torrent_startup['qbittorrent'] = qbittorrent_startup


# function that returns smallest list of all episode numbers that includes given episode
def get_episode_list(driver, ep):
    # press show more till we can see the start episode
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="' + ep + '"]')
            break  # if we can find start, it'll break from loop

        except NoSuchElementException:  # Thrown if driver can't find start

            try:
                driver.find_element_by_xpath('//*[@class="show-more"]/a').click()  # click on "show more" button
                sleep(0.7)
            except NoSuchElementException:  # Thrown if there's no more to show
                break

    # Create a list of all episode numbers visible
    return list(map(lambda x: x.get_attribute('id'), driver.find_elements_by_xpath('//*[@class="hs-shows"]/div')))


# function that iterates through a list of episodes and starts downloads of each
def start_downloads(episodes, driver, path):
    i = 0   # number of episodes downloaded
    for ep in episodes:
        try:
            # open magnet link of ep in preferred quality of user
            os.startfile(
                driver.find_element_by_xpath(
                    '//*[@id="' + ep + '-' + preferences['quality'] + '"]/span[2]/a').get_attribute
                ('href')
            )
        except NoSuchElementException:  # thrown if no magnet link of required quality found
            print("No Download link for episode", ep, preferences['quality'], "T-T")
            continue

        # start downloading torrent from your preferred software
        torrents[preferences['torrent']](path)

        # give confirmation message to user on terminal
        print("Downloading episode", ep, "now :)")

        i += 1  # increase number of episodes downloaded

    return i
