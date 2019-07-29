# python script to download a batch of episodes

# add horriblehome to sys.path
import sys
import os

sys.path.append(os.path.expandvars('%horriblehome%'))

from bs4 import BeautifulSoup as bs
import requests
from horriblefiles.user_preferences import preferences
import re
import horriblefiles.horrible_functions as hf
from pyautogui import getWindowsWithTitle

# get a list of ALL shows available on horriblesubs.info
# make sure iDOLM@STER doesn't get replaced by [email protected]
tags = bs(requests.get("https://horriblesubs.info/shows/").text,
          features='html.parser').select('div [class = "ind-show"] > a')
all_shows = list(map(lambda x: x.text.replace('[email protected]', 'iDOLM@STER'), tags))
for i in range(len(all_shows)):
    if all_shows[i].find(chr(8211)) != -1:
        all_shows[i] = all_shows[i].replace(chr(8211), chr(45))

# Take name of anime to download and validate
while True:
    name = input('\nEnter name of anime as written in the show library of horriblesubs.info'
                 '\nLink to show library - https://horriblesubs.info/shows/'
                 '\nName : ').replace(chr(8211), chr(45))

    if name not in all_shows:
        print('This anime cannot be found in the horriblesubs.info library')
        continue

    else:
        break

start = end = 0

# take input of which episode to start from
while True:
    start = input("\nEnter the starting episode (Press 0 to start from first episode) : ")
    if int(start) < 0:
        print("Invalid episode number")
    elif start == '0':  # get first episode released
        soup = bs(requests.get('https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') +
                               '+' + preferences['quality'] + '&s=id&o=asc').text, features='html.parser')
        # get name of first ep released
        epNames = soup.select('tr.success > td:nth-child(2)')
        for epName in epNames:
            title = [i.text for i in epName.findChildren('a') if not i.findChild('i')][0]
            print(title)
            if re.match('[HorribleSubs] '+name+' - \d+ [.+].mkv', title):
                # get the ep number from that name
                start = int(re.compile(' - \d+ \[').findall(title)[0].replace(' - ', '').replace(' [', ''))
                print(start)
                break
    else:
        # check if ep exists
        soup = bs(requests.get('https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') + '+' + start +
                               '+' + preferences['quality']).text, features='html.parser')
        if (len(soup.select('td[class="success"]'))) == 0:
            print('Cannot find episode')
            continue
        start = int(start)
        break

# take input of which episode to end at from
while True:
    end = input("\nEnter the ending episode (Press 0 to end at last episode) : ")
    if int(end) < 0:
        print("Invalid episode number")
    elif end == '0':  # get last episode released
        soup = bs(requests.get('https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') +
                               '+' + preferences['quality'] + '&s=id&o=desc').text, features='html.parser')
        # get name of last ep released
        epName = soup.select_one('tr.success:nth-child(1) > td:nth-child(2) > a:nth-child(1)').text
        # get the ep number from that name
        end = int(re.compile(' - \d+ \[').findall(epName)[0].replace(' - ', '').replace(' [', ''))
        print(end)
        break
    else:
        # check if ep exists
        soup = bs(requests.get('https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') + '+' + end +
                               '+' + preferences['quality']).text, features='html.parser')
        if (len(soup.select('td[class="success"]'))) == 0:
            print('Cannot find episode')
            continue
        end = int(end)
        break

# define path where episode is to be downloaded
path = preferences['download_path'] + name
if not os.path.exists(path):
    os.mkdir(path)  # if directory doesn't exist, make one

# start downloads
print('\nStarting Downloads')
for i in range(start, end+1):
    ep = str(i)
    if len(ep) == 1:
        ep = '0' + ep

    soup = bs(requests.get(
        'https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') + '+' + ep + '+' + preferences[
            'quality']).text, features='html.parser')
    links = [i.get('href') for i in soup.select('td[class="text-center"] > a')
             if 'fa-magnet' in i.findChild('i').get('class')]

    for link in links:
        os.startfile(link)
        hf.torrents[preferences['torrent']](path)

# close μTorrent
window = getWindowsWithTitle('μTorrent')
if len(window) > 0:
    for w in window:
        w.close()
