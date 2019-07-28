# python script to download a batch of episodes

# add horriblehome to sys.path
import sys
import os

sys.path.append(os.path.expandvars('%horriblehome%'))

from bs4 import BeautifulSoup as bs
import requests
from horriblefiles.user_preferences import preferences
import re

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

end = int(input('\nDownload upto which episode? (Enter 0 to end on last episode) : '))
if i == 0:
    endPage = 1
    endIndex = 0
else:
    i = 1
    boo = True
    while boo:
        soup = bs(requests.get(
            'https://nyaa.si/user/HorribleSubs?f=0&c=1_2&q=' + name.replace(' ', '+') + '+' + preferences[
                'quality'] + '&p=' + str(i)).text, features='html.parser')

        eps = soup.select('tr[class="success"]')
        for j in range(len(eps)):
            epName = eps[j].findChildren('td')[1].findChildren('a')[-1].text
            ep = int(
                re.compile(' - \d+ \[').findall(epName)[0].replace(' - ', '').replace(' [', '')
            )
            if ep == end:
                endPage = i
                endIndex = j
                print(i, j)
                boo = False
                break

        i += 1
