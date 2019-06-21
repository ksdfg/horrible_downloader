# ***horrible downloader***

Automatically download all episodes of the currently airing anime that you are watching that you haven't already, as well as download multiple episodes of an anime without a batch file!

<hr />

## Pre-requisites

- ***Windows***<br/>
    horrible downloader currently only works on Windows systems.

- ***Python 3 and above***<br/>
    Link to download of installation file : https://www.python.org/downloads/
    
- ***Mozilla Firefox or Google Chrome***<br/>
    horrible downloader requires one of the above two browsers to be installed on your system. We are working to make this program get the required magnet links without having to open any browsers, but for now having one of these is essential.

- ***uTorrent or qBitTorrent***<br/>
    Using horrible downloader, you will be able to not only open magnet links but also automatically start their downloads in your default software! At this moment horrible downloader supports uTorrent and qBitTorrent, so ensure one of these two is associated with torrents in your system.

<hr />

## How to install

- First ensure that you have all the pre-requisite softwares.<br/><br/>
- Download all the required software files from here. Unzip them in any directory on your computer.<br/><br/>
- Run the `horrible_setup.py` file to start the installation process. Wait for the installer to install the required Python modules in your computer. This could take a while.
  - You can run the file by double clicking it, or going to the file directory in the cmd and running `python horrible_setup.py`<br/><br/>
- When the installer shows you a prompt to tell it which browser out of given two options would you like to use, type the name of your preferred browser and press enter. Wait for the installer to download the required web driver and unzip it. This could take a while.<br/><br/>
- When the installer shows you a prompt to tell it which software is associated with torrents in your system, type the name of the software associated with torrents and press enter. To find out which software is supported by your system -
  - Search for default apps in your search menu
  - Click on `Choose default apps by file type`
  - Search which file is associated with .torrent<br/><br/>
- Next, the installer should ask you where you want to store your downloaded anime. Copy & paste the path to the folder where you want it to save the downloaded episodes.
  - If you copy something, you can paste it on the terminal by just clicking `right click` on your mouse<br/><br/>
- Next, the installer should ask you what quality you want the downloaded episodes to be in. Do not foget the `p` when typing your answer!<br/><br/>
  
We have finished installing the software with your preferences! Now all we need to do is make a list of the currently ongoing anime that horrible downloader will check for new episodes each time you run it. Wait for the menu to come up, and from then on it's an easy and intuitive process where you can add anime to your list, remove anime from your list, change the episode from which downloads will start next time of an anime already in your list or clear your currently watching.

<hr />

## How to use

horrible downloader is very simple to use! You simply need to run `horrible_downloader.py`, which will lead you to a menu that lists down the possible tasks you can perform with this tool. We will now go through these :

- Check and download new episodes of anime in your currently watching list
  - Type `1` to start this task. This will basically go through all the shows in your currently watching list, check if any new episodes have been released and start downloading them if they have.<br/><br/>
- Batch download of episodes of an anime
  - Type `2` to start this task. This will allow you to download all episodes in a range - or all episodes released - of an anime on horriblesubs.info<br/><br/>
- Update currently watching list
  - Type `3` to start this task. This brings up the menu from the end of the end of the installation process. It allows you to add anime to your list, remove anime from your list, change the episode from which downloads will start next time of an anime already in your list or clear your currently watching.<br/><br/>

<hr />