# file to be run to setup horrible downloader
import os
import re
import sys

# install required modules
os.system('pip install -r horriblefiles\\requirements.txt')

# set path to directory having horrible_downloader as env variable
os.system('setx horriblehome "' + os.getcwd() + '"')
sys.path.append(os.getcwd())
os.system('cls')

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

f = open('horriblefiles/user_preferences.py', 'r')
pref = f.read()
f.close()

pref = re.sub("torrent': '.+'", "torrent': '"+torrent+"'", pref)
pref = re.sub("download_path': '.+'", "download_path': '"+download_path.replace("\\", "\\\\\\\\")+"\\\\\\\\'", pref)
pref = re.sub("quality': '.+'", "quality': '"+quality+"'", pref)

f = open('horriblefiles/user_preferences.py', 'w')
f.write(pref)
f.close()

# clear the terminal
os.system('cls')

# Make your currently watching list
print("We're done installing the basic softwares! Now let's make a list of anime you are watching this season :)"
      "\nPlease wait while we bring up the currently watching list updater...")

# schedule check of ongoing series
os.system(r'schtasks /create /sc minute /mo 15 /tn "horribletasks\check currently watching" /tr "\"' +
          sys.executable.replace('python.exe', 'pythonw.exe') + r'\" \"' + os.getcwd() +
          r'\horriblefiles\ongoing_downloader.pyw\""')
