import os
from time import sleep
import pyautogui as pog
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs
import requests
from currently_watching import shows
import horrible_functions as hf
from user_preferences import preferences

soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows.keys()]
if len(links) == 0:
    print("Nothing to download today! T-T")
    exit(0)

driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
driver.implicitly_wait(10)


for link in links:
    i = 0
    ep = str(shows[link.text])
    driver.get("https://horriblesubs.info" + link.get("href"))

    driver.find_element_by_css_selector('#hs-search > input').send_keys(ep)
    pog.press('enter')
    sleep(1)

    try:
        hf.episode_selector(driver, ep, preferences['browser']).click()
    except NoSuchElementException:
        print("New Episode of " + link.text + " has not yet released!!\n\n")
        continue

    sleep(1)
    try:
        hf.magnet_selector(driver, ep, preferences['quality'], preferences['browser']).click()
    except NoSuchElementException:
        print("New Episode of " + link.text + " has not yet released!!\n\n")
        continue

    sleep(1)
    pog.click(*preferences['clicks'][i])
    i += 1
    sleep(1)
    path = preferences['download_path'] + link.text
    if not os.path.exists(path):
        os.makedirs(path)

    hf.torrents[preferences['torrent']](i, path)

    shows[link.text] += 1

    sleep(1)
    pog.hotkey('alt', 'f4')
    sleep(2)

driver.close()


f = open("currently_watching.py", "w")
f.write("shows = " + str(shows).replace(", ", ",\n"))
f.close()
