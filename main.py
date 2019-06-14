from selenium import webdriver as wbd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests
import time

xpath = {
    'search': r'/html/body/div[2]/div/div['r'2]/div[2]/div['r''r'1]/div/main/div['r''r'1]/article/div'r'/div['r''r'4]/form/input',
    'episode': r'/html/body/div[2]/div/div['r'2]/div[2]/div['r''r'1]/div/main/div['r'1]/article/div/div['r'4]/div['r''r'1]/div/a',
    'magnet': r'/html/body/div[2]/div/div['r'2]/div[2]/div['r''r'1]/div/main/div['r'1]/article/div/div['r'4]/div['r''r''r'1]/div/div'r'/div['r'3]/span[2]/a '
         }

shows = [
    "Fruits Basket (2019)",
    "Senryuu Shoujo",
    "Midara na Ao-chan wa Benkyou ga Dekinai",
    "Hitoribocchi no Marumaru Seikatsu",
    "Black Clover",
    "Isekai Quartet",
    "Sewayaki Kitsune no Senko-san",
    "Tate no Yuusha no Nariagari",
    "Kenja no Mago",
    "Amazing Stranger",
    "Joshikausei",
    "Nobunaga-sensei no Osanazuma",
    "Kimetsu no Yaiba",
    "Bokutachi wa Benkyou ga Dekinai"
]

soup = bs(requests.get("https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows]

driver = wbd.Firefox()

for link in links:

    if link.text in shows:

        print(link.get("href"))
        driver.get("https://horriblesubs.info" + link.get("href"))

        '''
        try:
            WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, xpath['search'])))
            b = driver.find_element_by_xpath(xpath['search'])
            b.send_keys("1"+Keys.ENTER)
        except TimeoutException:
            print("problem in", "search")
        '''

        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, xpath['search'])))
        time.sleep(15)
        b = driver.find_element_by_xpath(xpath['search'])
        b.send_keys("1"+Keys.ENTER)


        try:
            WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, xpath['episode'])))
        except TimeoutException:
            print("problem in", "episode")
        #time.sleep(2)
        b = driver.find_element_by_xpath(xpath['episode'])
        b.click()

        try:
            WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, xpath['magnet'])))
        except TimeoutException:
            print("problem in", "episode")
        #time.sleep(2)
        b = driver.find_element_by_xpath(xpath['magnet'])
        b.click()
        #break
