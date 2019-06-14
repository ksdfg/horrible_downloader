from selenium import webdriver as wbd
from selenium.common.exceptions import NoSuchElementException
import pyautogui as pog
from bs4 import BeautifulSoup as bs
import requests
from time import sleep
import os
from currently_watching import shows

soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows.keys()]

driver = wbd.Firefox(executable_path=r"C:\Users\ksdfg\AppData\Local\Programs\Python\Python37\Lib\site-packages"
                                     r"\selenium\webdriver\firefox\geckodriver.exe")
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
        driver.find_element_by_css_selector(r'.rls-label').click()
    except NoSuchElementException:
        print("Episode not yet released")
        continue

    sleep(1)
    try:
        driver.find_element_by_css_selector(r'#\3' + ep[0] + ' ' + ep[1:] + '-1080p > span:nth-child(2) > a:nth-child(1)').click()
    except NoSuchElementException:
        print("Episode not yet released")
        continue

    sleep(1)
    pog.click(780, 522)

    path = 'K:\\Videos\\' + link.text
    if not os.path.exists(path):
        os.mkdir(path)

    sleep(3)
    pog.typewrite(path)
    pog.press('enter')
    sleep(5)
    pog.press('enter')

    shows[link.text] += 1

    sleep(2)
    pog.hotkey('alt', 'f4')

driver.close()

f = open("currently_watching.py", "w")
f.write("shows = " + str(shows).replace(", ", ",\n"))
f.close()
