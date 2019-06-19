# python script to update your currently watching list
import os
from bs4 import BeautifulSoup as bs
import requests
import horriblefiles.horrible_functions as hf
from horriblefiles.user_preferences import preferences
from selenium.common.exceptions import NoSuchElementException

# get a list of ALL shows available on horriblesubs.info
# make sure iDOLM@STER doesn't get replaced by [email protected]
all_shows = list(map(lambda x: x.text.replace('[email protected]', 'iDOLM@STER'),
                      bs(requests.get("https://horriblesubs.info/shows/").text,
                         features='html.parser').select('div [title = "ind-show"] > a')
                      ))
while True:
    name = input('\nEnter name of anime as written in the show library of horriblesubs.info'
                 '\nLink to schedule - https://horriblesubs.info/shows/'
                 '\nName : ')

    if name not in all_shows:
        print('This anime cannot be found in the horriblesubs.info library')
        continue

    else: break

# parse html source of horriblesubs.info shows page
soup = bs(requests.get("https://horriblesubs.info/shows/" + name.replace(" ", "-") + "/").text, features='html.parser')

# list of all anime that are released today and are in your currently watching shows
latest = soup.select('a > strong').text

# define path where episode is to be downloaded
path = preferences['download_path'] + name
if not os.path.exists(path):
    os.mkdir(path)  # if directory doesn't exist, make one


while True:
    start = int(input("Enter the starting episode :  (Press 0 to start from first episode)"))
    if start == 0:
        print()
    elif start < 0:
        print("Invalid episode number")
    elif start > latest:
        print("Start episode cannot be greater than the last episode of Anime")
    else:
        break

while True:
    end = int(input("Enter the ending episode :  (Press 0 to start from first episode)"))
    if end == 0:
        end = int(latest)
    elif end < 0:
        print("Invalid episode number")
    elif end > latest:
        print("Ending episode number has not been released yet")
    else:
        break


# startup procedure for torrent software
hf.torrent_startup[preferences['torrent']]()

# open a web driver according to browser preference
driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
driver.implicitly_wait(10)  # make driver inherently wait for 10s after opening a page
os.system('cls')

for ep in range(start,end+1):
    try:
        os.startfile(
            driver.find_element_by_xpath(
                '//*[@id="' + ep + '-' + preferences['quality'] + '"]/span[2]/a').get_attribute
            ('href')
        )
    except NoSuchElementException:  # thrown if no magnet link of required quality found
        print("No Download link for episode", ep, preferences['quality'], "T-T")
        continue

    # start downloading torrent from your preferred software
    hf.torrents[preferences['torrent']](path)

    # give confirmation message to user on terminal
    print("Downloading episode", ep, "now :)")

driver.close()  # once you have checked all animes in links, close the web driver

# Give the user time to read status report
print('\nPress enter to quit! :)')
input()

# kill the chromedriver that doesn't kill itself...
os.system('taskkill /im "chromedriver.exe" /f')
