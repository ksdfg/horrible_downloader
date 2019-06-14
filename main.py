import os
from time import sleep
import pyautogui as pog
from selenium import webdriver



page = input("Enter the anime name :  ").lower().replace(" ", "-") + "/#" + input("Enter the episode number: ").rjust(2, "0")

driver = webdriver.Chrome(r'C:\Users\admin\Desktop\chromedriver')
driver.implicitly_wait(10)
driver.get("https://horriblesubs.info/shows/" + page)

driver.find_element_by_css_selector('#hs-search > input').send_keys(page[-2:])
pog.press('enter')
sleep(1)
driver.find_element_by_xpath('//*[@id="' + page[-2:] + '"]/a').click()
sleep(1)
driver.find_element_by_xpath('//*[@id="'+ page[-2:] + '-1080p"]/span[2]/a').click()
sleep(1)
pog.click(519, 200)
sleep(1)
pog.click(325, 396)
sleep(1)
path = "F:\Anime\\" + page.replace("-", " ")[:page.index('/#')]
if not os.path.exists(path):
    os.makedirs(path)

sleep(2)
pog.click(1034,216)
pog.typewrite(path)
pog.press('enter')
sleep(1)
pog.press('enter')
sleep(1)
pog.press('enter')

sleep(5)
pog.hotkey('ctrl', 'w')
