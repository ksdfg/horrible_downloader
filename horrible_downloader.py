# main menu
import os
import re

while True:

    print('\n1. Check and download new episodes of anime in your currently watching list\t(type 1 to select this)'
          '\n2. Batch download of episodes of an anime\t(type 2 to select this)'
          '\n3. Update currently watching list\t(type 3 to select this)'
          '\n4. Update preferences\t(type 3 to select this)'
          '\n5. Exit\t(type 4 to select this)')  # printing options
    choice = input('\nChoice : ')

    if choice == '5':
        exit(0)

    elif choice == '1':
        print('\nStarting checks...\n')
        import horriblefiles.ongoing_downloader

    elif choice == '2':
        print('\nStarting the batch downloader...')
        import horriblefiles.batch_downloader

    elif choice == '3':
        print('\nBringing up the currently watching list updater...')
        import horriblefiles.update_anime

    elif choice == '4':

        print(
            '\n1. Change Torrent Software'
            '\n2. Change Download Folder'
            '\n3. Change Quality'
            '\n4. Exit'
        )
        choice = input('\nChoice : ')

        if choice == '4':
            continue

        elif choice == '1':
            while True:
                torrent = input('\nhorrible downloader right now supports two torrent downloading software - '
                                'uTorrent and qBitTorrent.'
                                '\nWe require you to tell us which one is associated with magnet files in your'
                                ' system.'
                                '\nPlease make sure the spelling of your option matches the two options given'
                                ' above.'
                                '\nTorrent Downloading Software : ').lower()
                if torrent in ['utorrent', 'qbittorrent']:
                    break
                else:
                    print('Invalid response. Please check the spelling of your response and try again.')

            f = open(r'horriblefiles/user_preferences.py', 'r')
            pref = f.read()
            f.close()

            pref = re.sub("torrent': '.+'", "torrent': '" + torrent + "'", pref)

            f = open(r'horriblefiles/user_preferences.py', 'w')
            f.write(pref)
            f.close()

        elif choice == '2':
            while True:
                download_path = input('\nEnter path of the folder where you want your anime to be downloaded : ')
                if os.path.exists(download_path):
                    break
                else:
                    print('Invalid path. Please make sure the folder actually exists and try again')

            f = open(r'horriblefiles/user_preferences.py', 'r')
            pref = f.read()
            f.close()

            pref = re.sub("download_path': '.+'", "download_path': '" + download_path.replace("\\", "\\\\\\\\") +
                          "\\\\\\\\'", pref)

            f = open(r'horriblefiles/user_preferences.py', 'w')
            f.write(pref)
            f.close()

        elif choice == '3':
            while True:
                quality = input('\nYou can download episodes in 1080p, 720p or 480p.'
                                '\nChoose what quality you want to download your anime in : ')
                if quality in ['1080p', '720p', '480p']:
                    break
                else:
                    print('Invalid response. Please make sure your answer is one of the three options given and'
                          ' try again')

            f = open(r'horriblefiles/user_preferences.py', 'r')
            pref = f.read()
            f.close()

            pref = re.sub("quality': '.+'", "quality': '"+quality+"'", pref)

            f = open(r'horriblefiles/user_preferences.py', 'w')
            f.write(pref)
            f.close()

    else:
        print('Invalid option. Please try again.')
