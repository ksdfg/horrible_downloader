import os
from time import sleep
import pyautogui as pog
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import requests
from currently_watching import shows
import horrible_functions as hf
from user_preferences import preferences

# parse html source of horriblesubs homepage
soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

# list of all anime that are released today and are in your currently watching shows
links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows.keys()]
if len(links) == 0:
    print("Nothing to download today T-T")
    exit(0)

# open a web driver according to browser preference
driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
driver.implicitly_wait(10)  # make driver inherently wait for 10s after opening a page

# read the contents of currently watching file
f = open('currently_watching.py', 'r+')
cw = f.read()
f.close()

# iterate for each link
for link in links:

    print("\n" + link.text)     # print name of anime you are checking

    # var that stores which episode you are trying to download
    ep = str(shows[link.text])
    if len(ep) == 1:
        ep = '0' + ep

    # open the page in web driver
    driver.get("https://horriblesubs.info" + link.get("href") + "/#" + str(shows[link.text]))

    # enter episode number in the search bar
    driver.find_element_by_css_selector('#hs-search > input').send_keys(ep)
    pog.press('enter')

    # select which episode you want to download (from search results), and view download links
    sleep(2)
    try:
        hf.episode_selector(driver, ep, preferences['browser']).click()
    except NoSuchElementException:  # thrown if no results found
        print("No Download link for episode", ep, preferences['quality'], "T-T")
        continue

    # select which magnet link you want to open, and open it
    sleep(2)
    try:
        hf.magnet_selector(driver, ep, preferences['quality'], preferences['browser']).click()
    except NoSuchElementException:  # thrown if no magnet link of required quality found
        print("No Download link for episode", ep, preferences['quality'], "T-T")
        continue

    # click on the okay button to open your torrent downloading software
    sleep(1)
    pog.press(hf.torrent_opener[preferences['browser']])

    # define path where episode is to be downloaded
    path = preferences['download_path'] + link.text
    if not os.path.exists(path):
        os.mkdir(path)  # if directory doesn't exist, make one

    # start downloading torrent from your preferred software
    hf.torrents[preferences['torrent']](path)

    # give confirmation message to user on terminal
    print("Downloading episode", ep, "now :)")

    # next time try to download the next episode by updating currently watching
    cw = cw.replace((link.text + '": ' + str(shows[link.text])), (link.text + '": ' + str(shows[link.text]+1)))

driver.close()  # once you have checked all animes in links, close the web driver

# update the currently watching list
f = open("currently_watching.py", "w")
f.write(cw)
f.close()
