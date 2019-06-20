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

print('\nOpening', name, 'in web driver...')

# open a web driver according to browser preference
driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
driver.implicitly_wait(10)  # make driver inherently wait for 10s after opening a page
os.system('cls')

# parse html source of horriblesubs.info shows page
driver.get("https://horriblesubs.info" + tags[all_shows.index(name)].get('href'))

# get last episode released
last = driver.find_element_by_xpath('//*[@class="hs-shows"]/div[1]').get_attribute('id').split('v')[0]
hotkey('alt', '\t')     # bring focus back to downloader from driver

# take input of which episode to start from
while True:
    start = input("\nEnter the starting episode (Press 0 to start from first episode) : ")
    if int(start) < 0:
        print("Invalid episode number")
    elif int(start) > int(last):
        print("Start episode cannot be greater than the last episode of Anime")
    else:
        if len(start) is 1:
            start = '0' + start
        break

# take input of which episode to end with
while True:
    end = input("\nEnter the ending episode (Press 0 to end on last episode) : ")
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

# Create smallest list of all episode numbers that includes given episode
print('\nGetting list of episodes of', name, '...')
episodes = hf.get_episode_list(driver, start)

if start == '00':
    start = episodes[-1]    # set starting episode to first ep released in horrible

# get index of start (made for the cases when only v2 of an ep is available)
start_ind = -1
for i in range(len(episodes)):
    if episodes[i].find(start) > -1:
        start_ind = i
        break

# get index of end (made for the cases when only v2 of an ep is available)
end_ind = -1
for i in range(len(episodes)):
    if episodes[i].find(end) > -1:
        end_ind = i
        break

episodes = episodes[end_ind: start_ind+1]   # list of all eps we need to download

# define path where episode is to be downloaded
path = preferences['download_path'] + name
if not os.path.exists(path):
    os.mkdir(path)  # if directory doesn't exist, make one

# startup procedure for torrent software
hf.torrent_startup[preferences['torrent']]()

# loop to start all downloads
print('\nStarting downloads...\n')
hf.start_downloads(episodes, driver, path)

driver.close()  # once you have checked all animes in links, close the web driver

# Give the user time to read status report
input('\nPress enter to quit! :)')

# kill the chromedriver that doesn't kill itself...
os.system('taskkill /im "chromedriver.exe" /f')
