# python script to update your currently watching list
import os
from bs4 import BeautifulSoup as bs
import requests
import horriblefiles.horrible_functions as hf
from horriblefiles.user_preferences import preferences
from selenium.common.exceptions import NoSuchElementException
from pyautogui import hotkey

# get a list of ALL shows available on horriblesubs.info
# make sure iDOLM@STER doesn't get replaced by [email protected]
tags = bs(requests.get("https://horriblesubs.info/shows/").text,
          features='html.parser').select('div [class = "ind-show"] > a')
all_shows = list(map(lambda x: x.text.replace('[email protected]', 'iDOLM@STER'),tags))

# Take name of anime to download and validate
while True:
    name = input('\nEnter name of anime as written in the show library of horriblesubs.info'
                 '\nLink to show library - https://horriblesubs.info/shows/'
                 '\nName : ')

    if name not in all_shows:
        print('This anime cannot be found in the horriblesubs.info library')
        continue

    else:
        break

# open a web driver according to browser preference
driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
driver.implicitly_wait(10)  # make driver inherently wait for 10s after opening a page
os.system('cls')

# parse html source of horriblesubs.info shows page
driver.get("https://horriblesubs.info" + tags[all_shows.index(name)].get('href'))

last = driver.find_element_by_xpath('//*[@class="hs-shows"]/div[1]').get_attribute('id').split('v')[0]
hotkey('alt', '\t')

while True:
    start = input("Enter the starting episode :  (Press 0 to start from first episode)")
    if int(start) < 0:
        print("Invalid episode number")
    elif int(start) > int(last):
        print("Start episode cannot be greater than the last episode of Anime")
    else:
        if len(start) is 1:
            start = '0' + start
        break

while True:
    end = input("Enter the ending episode :  (Press 0 to end on last episode)")
    if end is '0':
        end = last
        break
    elif int(end) < 0:
        print("Invalid episode number")
    elif int(end) > int(last):
        print("Ending episode number has not been released yet")
    elif int(end) < int(start):
        print("You cannot end before you start")
    else:
        if len(end) is 1:
            end = '0' + end
        break

while True:
    try:
        driver.find_element_by_xpath('//*[@id="' + start + '"]')
        break

    except NoSuchElementException:

        try:
            driver.find_element_by_xpath('//*[@class="show-more"]/a').click()
        except NoSuchElementException:
            break

episodes = list(map(lambda x: x.get_attribute('id'), driver.find_elements_by_xpath('//*[@class="hs-shows"]/div')))

if start == '00':
    start = episodes[-1]

start_ind = 0
for i in range(len(episodes)):
    if episodes[i].find(start) > -1:
        start_ind = i
        break

end_ind = 0
for i in range(len(episodes)):
    if episodes[i].find(end) > -1:
        end_ind = i
        break

episodes = episodes[end_ind: start_ind+1]
print(episodes)

# define path where episode is to be downloaded
path = preferences['download_path'] + name
if not os.path.exists(path):
    os.mkdir(path)  # if directory doesn't exist, make one

# startup procedure for torrent software
hf.torrent_startup[preferences['torrent']]()

for ep in episodes:
    try:
        print('\nstarting download', ep)
        os.startfile(
            driver.find_element_by_xpath(
                '//*[@id="' + ep + '-' + preferences['quality'] + '"]/span[2]/a').get_attribute
            ('href')
        )
    except NoSuchElementException:  # thrown if no magnet link of required quality found
        print("No Download link for episode", ep, preferences['quality'], "T-T")
        continue

    # start downloading torrent from your preferred software
    hf.torrents[preferences['torrent']](path)

    # give confirmation message to user on terminal
    print("Downloading episode", ep, "now :)")

driver.close()  # once you have checked all animes in links, close the web driver

# Give the user time to read status report
print('\nPress enter to quit! :)')
input()

# kill the chromedriver that doesn't kill itself...
os.system('taskkill /im "chromedriver.exe" /f')
