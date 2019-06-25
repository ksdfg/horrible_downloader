import subprocess
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime as dt, timedelta as td

day = 5 + (2 * dt.today().weekday())

soup = bs(requests.get('https://horriblesubs.info/release-schedule/').text, features='html.parser')

tr = soup.select('div [class="entry-content"] > table:nth-child({}) > tr'.format(day))

times = set()

for i in tr:
    hs = list(map(int, i.findChildren('td')[1].text.split(':')))
    print(hs)
    time = str((dt.now() + td(hours=hs[0], minutes=hs[1])).time()).split(':')
    times.add('{}:{}'.format(time[0], time[1]))
