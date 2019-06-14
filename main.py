import os
from time import sleep
import pyautogui as pog
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup as bs
import requests
from currently_watching import shows

soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows.keys()]
if len(links) == 0:
    print("Nothing to download today! T-T")
    exit(0)

#page = input("Enter the anime name :  ").lower().replace(" ", "-") + "/#" + input("Enter the episode number: ").rjust(2, "0")

driver = webdriver.Chrome(r'E:\Applications\chromedriver.exe')
driver.implicitly_wait(10)

for link in links:

    ep = str(shows[link.text])
    driver.get("https://horriblesubs.info" + link.get("href"))

    driver.find_element_by_css_selector('#hs-search > input').send_keys(ep)
    pog.press('enter')
    sleep(1)

    try:
        driver.find_element_by_xpath('//*[@id="' + ep + '"]/a').click()
    except NoSuchElementException:
        pog.hotkey('ctrl', 'w')
        print("New Episode of " + link.text + " has not yet released!!\n\n")
        continue

    sleep(1)
    driver.find_element_by_xpath('//*[@id="'+ ep + '-1080p"]/span[2]/a').click()
    sleep(1)
    pog.click(519, 200)
    sleep(1)
    pog.click(325, 396)
    sleep(1)
    path = "F:\Anime\\" + link.text
    if not os.path.exists(path):
        os.makedirs(path)

    sleep(2)
    pog.click(1020,216)
    pog.hotkey('ctrl', 'a')
    pog.typewrite(path)
    pog.press('enter')
    sleep(1)
    pog.press('enter')

    shows[link.text] += 1

    sleep(5)
    pog.hotkey('alt', 'f4')
    sleep(2)
try:
    driver.close()
except WebDriverException:
    sleep(0.01)

f = open("currently_watching.py", "w")
f.write("shows = " + str(shows).replace(", ", ",\n"))
f.close()
