from selenium import webdriver as wbd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests


def getElem(xpath, elem):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))

    try:
        WebDriverWait(driver, 60).until(element_present)
    except TimeoutException:
        print("problem in ", elem)

    return driver.find_element_by_xpath(xpath)


shows = ["Fruits Basket (2019)", "Senryuu Shoujo", "Midara na Ao-chan wa Benkyou ga Dekinai", "Hitoribocchi no "
                                                                                              "Marumaru Seikatsu"]

soup = bs(requests.get(
    "https://horriblesubs.info/").text, features='html.parser')

links = [i for i in soup.select('a[title = "See all releases for this show"]') if i.text in shows]

driver = wbd.Firefox()

for link in links:
    
    if link.text in shows:
        print(link.get("href"))
        driver.get("https://horriblesubs.info/" + link.get("href"))

        getElem(r'/html/body/div[2]/div/div[2]/div[2]/div[1]/div/main/div['r'1]/article/div/div[4]/form/input', "search").send_keys("1"+Keys.ENTER)

        getElem(r'/html/body/div[2]/div/div[2]/div[2]/div[1]/div/main/div[1]/article/div/div['r'4]/div[1]/div/a', "episode").click()

        getElem(r'/html/body/div[2]/div/div[2]/div[2]/div[1]/div/main/div[1]/article/div/div['r'4]/div['r'1]/div/div'r'/div[3]/span[2]/a', "magnet").click()
        #break