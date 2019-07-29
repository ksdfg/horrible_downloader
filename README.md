# ***horrible downloader***

Automatically download all episodes of the currently airing anime that you are watching that you haven't already, as well as download multiple episodes of an anime without a batch file!

<hr />

## Pre-requisites

- ***Windows***<br/>
    horrible downloader currently only works on Windows systems, and it's been tested on Windows 10.

- ***Python 3 and above***<br/>
    Link to download of installation file : https://www.python.org/downloads/<br/>
    While installing, before clicking on `Install Now` option, make sure to select the `Add Python to path` option given below.
 
- ***uTorrent or qBitTorrent***<br/>
    Using horrible downloader, you will be able to not only open magnet links but also automatically start their downloads in your default software! At this moment horrible downloader supports uTorrent and qBitTorrent, so ensure one of these two is associated with torrents in your system.

<hr />

## How to install

- First ensure that you have all the pre-requisite softwares.<br/><br/>
- Download horrible_downloader.zip from the releases tab. Unzip it in any directory on your computer.<br/><br/>
- Run the `horrible_setup.py` by double clicking it file to start the installation process. Wait for the installer to install the required Python modules in your computer. This could take a while.<br/><br/>
- When the installer shows you a prompt to tell it which software is associated with torrents in your system, type the name of the software associated with torrents and press enter. To find out which software is supported by your system -
  - Search for default apps in your search menu
  - Click on `Choose default apps by file type`
  - Search which file is associated with .torrent<br/><br/>
- Next, the installer should ask you where you want to store your downloaded anime. Copy & paste the path to the folder where you want it to save the downloaded episodes.
  - If you copy something, you can paste it on the terminal by just clicking `right click` on your mouse<br/><br/>
- Next, the installer should ask you what quality you want the downloaded episodes to be in. Do not forget the `p` when typing your answer!<br/><br/>
  
We have finished installing the software with your preferences! Now all we need to do is make a list of the currently ongoing anime that horrible downloader will check for new episodes each time you run it. Wait for the menu to come up, and from then on it's an easy and intuitive process where you can add anime to your list, remove anime from your list, change the episode from which downloads will start next time of an anime already in your list or clear your currently watching.

<hr />

## How to use

horrible downloader is very simple to use! You simply need to run `horrible_downloader.py`, which will lead you to a menu that lists down the possible tasks you can perform with this tool. We will now go through these :

- Check and download new episodes of anime in your currently watching list
  - Type `1` to start this task. This will basically go through all the shows in your currently watching list, check if any new episodes have been released and start downloading them if they have.
  - This task can download multiple episodes of a single series. For example, if you have set a series to start downloading from ep. 9 in the next check but the latest episode of the series released was ep. 13, then horrible downloader will download all episodes from 9 - 13 and set ep. 14 to be downloaded in the next check.<br/><br/>
- Batch download of episodes of an anime
  - Type `2` to start this task. This will allow you to download all episodes in a range - or all episodes released - of an anime on horriblesubs.info<br/><br/>
- Update currently watching list
  - Type `3` to start this task. This brings up the menu from the end of the end of the installation process. It allows you to add anime to your list, remove anime from your list, change the episode from which downloads will start next time of an anime already in your list or clear your currently watching.<br/><br/>

<hr />

## Scheduled Checks

Every 15 minutes, horrible downloader checks to see if any new episodes of the anime in your currently watching list have been released. If they have, a popup appears which asks if you want to start the downloads. The checks occur in the background and won't disturb your day-to-day usage of your pc. This way you will be able to download new episodes as soon as you can! If the check does find new episodes to download, then it will create a popup that asks if you want to start downloads now and then wait for 1 minute. If you do not press okay in 1 minute then it will cancel the download.<br/><br/>

<hr />
