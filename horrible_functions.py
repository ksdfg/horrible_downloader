# This file basically has all the functions and variables that allow our system to be modular
# Which functions / variables are used depends on the user's preference settings

from user_preferences import preferences
from selenium import webdriver as wbd
from time import sleep
import pyautogui as pog

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


# Function for when magnet link is opened in utorrent
def utorrent_download(path):
    sleep(3)
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press('enter')
    sleep(5)
    pog.press('enter')


# Function for when magnet link is opened in qbittorrent
def qbittorrent_download(i, path):
    sleep(3)
    pog.click(*preferences['clicks'][i])
    i += 1
    sleep(2)
    pog.click(*preferences['clicks'][i])
    i += 1
    pog.typewrite(path)     # enter path where you want to store the downloaded episode
    pog.press('enter')
    sleep(1)
    pog.press('enter')
    pog.press('enter')
    sleep(2)


# dictionary to decide which function should be called to start torrent download
torrents = {
    'utorrent': utorrent_download,
    'qbittorrent': qbittorrent_download
}

# the comment you have to write to currently watching.... this was dumb
cw_comment = '# This is the list of shows you are currently watching this season\n# The syntax is "show\'s name": ' \
             'next episode to be downloaded\n# e.g. : "JoJo\'s Bizarre Adventure - Golden Wind": 35\n# This means ' \
             'that I already have downloaded ep. 34 and need to download ep.35\n# Please ensure that the show\'s name ' \
             'is exactly the same as it appears in HorribleSubs\' schedule\n\n'
