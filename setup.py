# file to be run to setup horrible downloader
from pip._internal import main as pipmain
import re
import os
import horrible_functions as hf

# install selenium if not already installed
pipmain(['install', 'selenium'])

# take input of what browser to use
while True:
    browser = input('\nhorrible downloader right now supports two browsers - Mozilla Firefox and Google Chrome.'
                    '\nWe require you to choose which one horrible downloader will use.'
                    '\nBrowser : ').lower()
    # select correct browser according to user input
    if re.search('firefox', browser):
        browser = 'firefox'
        break
    elif re.search('chrome', browser):
        browser = 'chrome'
        break
    else:
        print('Invalid response. Please check your answer is one of the provided options and try again')

# Take input of driver_path
while True:
    driver_path = input('\nEnter path of download location of web driver : ')
    if os.path.exists(driver_path):
        break
    else:
        print('Invalid path. Please make sure the folder actually exists and try again')

# installing web driver
driver_path = hf.download_driver[browser](driver_path)

# Take input of torrent downloading software used
while True:
    torrent = input('\nhorrible downloader right now supports two torrent downloading software - '
                    'uTorrent and qBitTorrent.'
                    '\nWe require you to tell us which one is associated with magnet files in your system.'
                    '\nPlease make sure the spelling of your option matches the two options given above.'
                    '\nTorrent Downloading Software : ').lower()
    if torrent in ['utorrent', 'qbittorrent']:
        break
    else:
        print('Invalid response. Please check the spelling of your response and try again.')

# Take input of path where all anime is to be downloaded
while True:
    download_path = input('\nEnter path of the folder where you want your anime to be downloaded : ')
    if os.path.exists(download_path):
        break
    else:
        print('Invalid path. Please make sure the folder actually exists and try again')

# Take input of Quality in which user wants to download episode
while True:
    quality = input('\nYou can download episodes in 1080p, 720p or 360p.'
                    '\nChoose what quality you want to download your anime in : ')
    if quality in ['1080p', '720p', '360p']:
        break
    else:
        print('Invalid response. Please make sure your answer is one of the three options given and try again')
