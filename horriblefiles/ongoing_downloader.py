# checks and downloads episodes of anime in the currently watching list

# add horriblehome to sys.path
import sys
import os
sys.path.append(os.path.expandvars('%horriblehome%'))

from horriblefiles.currently_watching import shows
import horriblefiles.horrible_functions as hf
from horriblefiles.user_preferences import preferences
from pyautogui import hotkey

# startup procedure for torrent software
hf.torrent_startup[preferences['torrent']]()

# read the contents of currently watching file
f = open(os.path.relpath(os.path.expandvars('%horriblehome%') + '\horriblefiles\currently_watching.py', os.getcwd()), 'r+')
cw = f.read()
f.close()

# open a web driver according to browser preference
driver = hf.drivers[preferences['browser']](executable_path=preferences['driver_path'])
# driver.implicitly_wait(10)  # make driver inherently wait for 10s after opening a page
os.system('cls')
hotkey('alt', '\t')

# iterate for each link
for i in shows.keys():

    print("\n" + i)     # print name of anime you are checking

    # var that stores which episode you are trying to download
    ep = str(shows[i][0])
    if len(ep) == 1:
        ep = '0' + ep

    # open the page in web driver
    driver.get("https://horriblesubs.info" + shows[i][1])

    # check if latest episode released is less than required episode
    latest = driver.find_element_by_xpath('//*[@class="hs-shows"]/div[1]').get_attribute('id')
    if int(latest) < shows[i][0]:
        print("Episode", ep, "not yet released T-T")
        continue

    # define path where episode is to be downloaded
    path = preferences['download_path'] + i
    if not os.path.exists(path):
        os.mkdir(path)  # if directory doesn't exist, make one

    # Create smallest list of all episode numbers that includes given episode
    print('Getting list of episodes to download...')
    episodes = hf.get_episode_list(driver, ep)

    episodes = episodes[:episodes.index(ep)+1]   # list of all eps we need to download
    no_eps = hf.start_downloads(episodes, driver, path)

    # next time try to download the next episode by updating currently watching
    cw = cw.replace((i + '": [' + str(shows[i][0])), (i + '": [' + str(shows[i][0]+no_eps)))

driver.close()  # once you have checked all animes in links, close the web driver

# update the currently watching list
f = open(os.path.relpath(os.path.expandvars('%horriblehome%') + '\horriblefiles\currently_watching.py', os.getcwd()), "w")
f.write(cw)
f.close()

# Give the user time to read status report
input('\nPress enter to quit! :)')

# kill the chromedriver that doesn't kill itself...
if preferences['browser'] == 'chrome':
    os.system('taskkill /im "chromedriver.exe" /f')
