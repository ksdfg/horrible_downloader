# main menu

import sys
import ctypes
from threading import Thread
from time import sleep
import os
from pyautogui import getWindowsWithTitle

# if it has been called by scheduler
if len(sys.argv) > 1:
    i = -1
    
    def meow():    # function to thread - wait for 10s, then start check
        sleep(10)
        if i==-1:
            getWindowsWithTitle('horrible downloader')[0].close()
            os.system('python "' + os.path.join(os.path.expandvars('%horriblehome%'), 'horriblefiles', 'ongoing_downloader.py') + '" arg')
    
    t = Thread(target=meow)
    t.start()
    
    i = ctypes.windll.user32.MessageBoxW(0, "Start checks of currently watching anime?", "horrible downloader", 0x1001)  # popup
    if i == 1:
        os.system('python "' + os.path.join(os.path.expandvars('%horriblehome%'), 'horriblefiles', 'ongoing_downloader.py') + '" arg')
        
    t.join()
    exit(0)

print('\n1. Check and download new episodes of anime in your currently watching list\t(type 1 to select this)'
      '\n2. Batch download of episodes of an anime\t(type 2 to select this)'
      '\n3. Update currently watching list\t(type 3 to select this)'
      '\n4. Exit\t(type 4 to select this)')     # printing options
choice = input('\nChoice : ')

if choice == '4':
    exit(0)

elif choice == '1':
    print('\nStarting checks...')
    import horriblefiles.ongoing_downloader

elif choice == '2':
    print('\nStarting the batch downloader...')
    import horriblefiles.batch_downloader

elif choice == '3':
    print('\nBringing up the currently watching list updater...')
    import horriblefiles.update_anime

else:
    print('Invalid option. Please try again.')
