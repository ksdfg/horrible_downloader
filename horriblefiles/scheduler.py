# schedule the day's checks of ongoing

# add horriblehome to sys.path
import sys
import os
sys.path.append(os.path.expandvars('%horriblehome%'))

from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime as dt, timedelta as td
from pytz import timezone
from tzlocal import get_localzone
from win32com.client import Dispatch
import horriblefiles.horrible_functions as hf
from horriblefiles.currently_watching import shows

day = {'Monday': 5, 'Tuesday': 7, 'Wednesday': 9, 'Thursday': 11, 'Friday': 13, 'Saturday': 15, 'Sunday': 17}

soup = bs(requests.get('https://horriblesubs.info/release-schedule/').text, features='html.parser')

tr = soup.select('div [class="entry-content"] > table:nth-child({}) > tr'.format(day[soup.select_one('#today').text.split()[0]]))

times = set()

for i in tr:
    if i.findChildren('td')[0].text in shows:
        hs = list(map(int, i.findChildren('td')[1].text.split(':')))
        times.add(((dt.now() + td(hours=hs[0], minutes=hs[1])).isoformat()))

# schedule the day's checks
hf.schedule(
    name='horrible downloader - ongoing check scheduler',
    description='Check if any new episode of the animes in your currently watching list have been released, and download them',
    path='"' + sys.executable.replace('python.exe', 'pythonw.exe') + '"',
    args=os.path.join('"' + os.path.expandvars('%horriblehome%'), 'horrible_downloader.py') + '" arg',
    times=times,
    repetition=1
)

# setup tomorrow's check
tza = timezone('America/Los_Angeles')   # create an instance of timezone in LA
tzl = get_localzone()                   # create an instance of timezone system is set to

# make a datetime object with today's date and time 00:00:00, then set it's timezone as LA
zero = tza.localize(dt(dt.today().year, dt.today().month, dt.today().day, 0, 0, 0) + td(days=1))

# create datetime object which converts above object into corr. datetime in local timezone
local_zero = zero.astimezone(tzl).isoformat()

# schedule check
hf.schedule(
    name='horrible downloader - daily check scheduler',
    description="Schedule the day's checks for new episode releases",
    path='"' + sys.executable.replace('python.exe', 'pythonw.exe') + '"',
    args=os.path.join('"' + os.path.expandvars('%horriblehome%'), 'horriblefiles', 'scheduler.py') + '"',
    times=[local_zero],
    repetition=2
)
