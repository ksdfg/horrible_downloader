from selenium import webdriver as wbd
from time import sleep
import pyautogui as pog

drivers = {
    'firefox': wbd.Firefox,
    'chrome': wbd.Chrome
}


def link_selector(webdriver, ep, browser):
    if browser == 'firefox':
        return webdriver.find_element_by_css_selector(r'.rls-label')
    elif browser == 'chrome':
        return webdriver.find_element_by_xpath('//*[@id="' + ep + '"]/a')


def magnet_selector(webdriver, ep, quality, browser):
    if browser == 'firefox':
        return webdriver.find_element_by_css_selector(r'#\3' + ep[0] + ' ' + ep[1:] + '-' + quality + '> span:nth-child(2) > ''a:nth-child(1)')
    elif browser == 'chrome':
        return webdriver.find_element_by_xpath('//*[@id="' + ep + '-1080p"]/span[2]/a')


def utorrent_download(path):
    sleep(3)
    pog.typewrite(path)
    pog.press('enter')
    sleep(5)
    pog.press('enter')


def qbittorrent_download(path):
    sleep(2)
    pog.click(1020, 216)
    pog.hotkey('ctrl', 'a')
    pog.typewrite(path)
    pog.press('enter')
    sleep(1)
    pog.press('enter')


torrents = {
    'utorrent': utorrent_download,
    'qbittorrent': qbittorrent_download
}