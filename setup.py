# file to be run to setup horrible downloader
import requests
from pip._internal import main as pipmain
import re
import os
import horrible_functions as hf
import zipfile
import io

# install required apis and modules if not already installed
pipmain(['install', 'selenium'])
print('\n')
pipmain(['install', 'pyautogui'])
print('\n')
pipmain(['install', 'beautifulsoup4'])
print('\n')
pipmain(['install', 'requests'])
print('\n')

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

# installing web driver
driver_path = os.path.join('C:\\', 'Users', os.getlogin(), 'AppData', 'Local', 'Programs', 'Python', 'Python37',
                           'Lib', 'site-packages', 'selenium', 'webdriver', browser)
print('Downloading web driver...')
# download file from github
win = '64' if 'PROGRAMFILES(X86)' in os.environ else '32'
r = requests.get(hf.download_driver[browser][0] + (win if browser=='firefox' else '') + '.zip', stream=True)
print('Downloaded zip file from the internet.\nExtracting zip file...')
r = zipfile.ZipFile(io.BytesIO(r.content))  # convert file to zip file
r.extractall(driver_path)   # extract zip file at given path
print('extracted zip file.')
driver_path += '\\' + hf.download_driver[browser][1] + '.exe'    # make driver path be path to driver.exe and return it

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
    quality = input('\nYou can download episodes in 1080p, 720p or 480p.'
                    '\nChoose what quality you want to download your anime in : ')
    if quality in ['1080p', '720p', '480p']:
        break
    else:
        print('Invalid response. Please make sure your answer is one of the three options given and try again')

f = open('user_preferences.py', 'r')
pref = f.read()
f.close()

pref = re.sub("browser': '.+'", "browser': '"+browser+"'", pref)
pref = re.sub("driver_path': r'.+'", "driver_path': r'"+driver_path.replace("\\", "\\\\")+"'", pref)
pref = re.sub("torrent': '.+'", "torrent': '"+torrent+"'", pref)
pref = re.sub("download_path': '.+'", "download_path': '"+download_path.replace("\\", "\\\\\\\\")+"\\\\\\\\'", pref)
pref = re.sub("quality': '.+'", "quality': '"+quality+"'", pref)

f = open('user_preferences.py', 'w')
f.write(pref)
f.close()
