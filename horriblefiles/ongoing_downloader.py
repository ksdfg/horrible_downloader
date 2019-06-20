# checks and downloads episodes of anime in the currently watching list

import os
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import requests
from horriblefiles.currently_watching import shows
import horriblefiles.horrible_functions as hf
from horriblefiles.user_preferences import preferences

# startup procedure for torrent software
hf.torrent_startup[preferences['torrent']]()

# read the contents of currently watching file
f = open('horriblefiles/currently_watching.py', 'r+')
cw = f.read()
f.close()

# open a web driver according to browser preference
driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
# driver.implicitly_wait(10)  # make driver inherently wait for 10s after opening a page
os.system('cls')

# iterate for each link
for i in shows.keys():

    print("\n" + i)     # print name of anime you are checking

    # var that stores which episode you are trying to download
    ep = str(shows[i][0])
    if len(ep) == 1:
        ep = '0' + ep

    # open the page in web driver
    driver.get("https://horriblesubs.info" + shows[i][1])

    # check if latest episode released is less than required episode
    latest = driver.find_element_by_xpath('//*[@class="hs-shows"]/div[1]').get_attribute('id')
    if int(latest) < shows[i][0]:
        print("Episode", ep, "not yet released T-T")
        continue

    try:
        os.startfile(
            driver.find_element_by_xpath('//*[@id="' + ep + '-' + preferences['quality'] + '"]/span[2]/a').get_attribute
            ('href')
        )
    except NoSuchElementException:  # thrown if no magnet link of required quality found
        print("No Download link for episode", ep, preferences['quality'], "T-T")
        continue

    # define path where episode is to be downloaded
    path = preferences['download_path'] + i
    if not os.path.exists(path):
        os.mkdir(path)  # if directory doesn't exist, make one

    # start downloading torrent from your preferred software
    hf.torrents[preferences['torrent']](path)

    # give confirmation message to user on terminal
    print("Downloading episode", ep, "now :)")

    # next time try to download the next episode by updating currently watching
    cw = cw.replace((i + '": ' + str(shows[i][0])), (i + '": ' + str(shows[i][0]+1)))

driver.close()  # once you have checked all animes in links, close the web driver

# update the currently watching list
f = open("horriblefiles/currently_watching.py", "w")
f.write(cw)
f.close()

# Give the user time to read status report
print('\nPress enter to quit! :)')
input()

# kill the chromedriver that doesn't kill itself...
if preferences['browser'] == 'chrome':
    os.system('taskkill /im "chromedriver.exe" /f')
