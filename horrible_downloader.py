from selenium.common.exceptions import NoSuchElementException
import pyautogui as pog
from bs4 import BeautifulSoup as bs
import requests
from time import sleep
import os
from currently_watching import shows
from user_preferences import preferences
import horrible_functions as hf

soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows.keys()]
if len(links) == 0:
    print("Nothing to download today T-T")
    exit(0)

driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
driver.implicitly_wait(10)

for link in links:

    print("\n", link.text, sep="")
    driver.get("https://horriblesubs.info" + link.get("href"))

    ep = str(shows[link.text])
    if len(ep) == 1:
        ep = '0' + ep

    driver.find_element_by_css_selector('#hs-search > input').send_keys(ep)
    pog.press('enter')

    sleep(1)
    try:
        hf.link_selector(driver, ep, preferences['browser']).click()
    except NoSuchElementException:
        print("Episode not yet released")
        continue

    sleep(1)
    try:
        hf.magnet_selector(driver, ep, preferences['quality'], preferences['browser']).click()
    except NoSuchElementException:
        print("Episode not yet released")
        continue

    sleep(1)
    pog.click(*preferences['clicks'][0])

    path = 'K:\\Videos\\' + link.text
    if not os.path.exists(path):
        os.mkdir(path)

    sleep(3)
    pog.typewrite(path)
    pog.press('enter')
    sleep(5)
    pog.press('enter')

    sleep(2)
    pog.hotkey('alt', 'f4')

    shows[link.text] += 1

driver.close()

f = open("currently_watching.py", "w")
f.write("shows = " + str(shows).replace(", ", ",\n"))
f.close()
