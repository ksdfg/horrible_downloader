from selenium import webdriver as wbd
from selenium.common.exceptions import NoSuchElementException
import pyautogui as pog
from bs4 import BeautifulSoup as bs
import requests
from time import sleep
import os

shows = {
    "Fruits Basket (2019)": 12,
    "Senryuu Shoujo": 12,
    "Midara na Ao-chan wa Benkyou ga Dekinai": 12,
    "Hitoribocchi no Marumaru Seikatsu": 12,
    "Black Clover": 88,
    "Isekai Quartet": 11,
    "Sewayaki Kitsune no Senko-san": 10,
    "Tate no Yuusha no Nariagari": 24,
    "Kenja no Mago": 11,
    "Amazing Stranger": 11,
    "Joshikausei": 11,
    "Nobunaga-sensei no Osanazuma": 11,
    "Kimetsu no Yaiba": 11,
    "Bokutachi wa Benkyou ga Dekinai": 11,
    "One Punch Man S2": 10
}

soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows.keys()


         ]

browser = wbd.Firefox()
browser.implicitly_wait(10)

for link in links:

    print("\n", link.text, sep="")
    browser.get("https://horriblesubs.info" + link.get("href"))

    browser.find_element_by_css_selector('#hs-search > input').send_keys('12')
    pog.press('enter')

    sleep(1)
    try:
        browser.find_element_by_css_selector(r'.rls-label').click()
    except NoSuchElementException:
        print("Episode not yet released")
        continue

    sleep(1)
    try:
        browser.find_element_by_css_selector(r'#\31 2-1080p > span:nth-child(2) > a:nth-child(1)').click()
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

    sleep(2)
    pog.hotkey('alt', 'f4')
    #break

browser.close()
