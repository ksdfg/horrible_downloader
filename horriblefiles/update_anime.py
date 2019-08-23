# python script to update your currently watching list

# add horriblehome to sys.path
import sys
import os

sys.path.append(os.path.expandvars('%horriblehome%'))

from horriblefiles.currently_watching import shows
from bs4 import BeautifulSoup as bs
import requests
import re

special_chars = ['+', '*', '.', '|', '(', ')', '$', '[', ']']  # set of all special chars in patterns

# interactive loop
while True:
    print('\n1. Add anime to currently watching list\t(type 1 to select this)'
          '\n2. Remove anime from currently watching\t(type 2 to select this)'
          '\n3. Change episode to start downloading from of anime in currently watching list\t(type 3 to select this)'
          '\n4. Clear currently watching list\t(type 4 to select this)'
          '\n5. Exit\t(type 5 to select this)')  # printing options
    choice = input('\nChoice : ')

    if choice == '5':  # user wants to exit
        break

    elif choice == '1':  # user wants to add anime to list

        # get a list of ALL currently airing shows
        # make sure iDOLM@STER doesn't get replaced by [email protected]
        tags = bs(requests.get("https://horriblesubs.info/release-schedule/").text,
                  features='html.parser').select('a[title = "See all releases for this show"]')
        curr_shows = list(map(lambda x: x.text.replace('[email protected]', 'iDOLM@STER'), tags))
        for i in range(len(curr_shows)):
            if curr_shows[i].find(chr(8211)) != -1:
                curr_shows[i] = curr_shows[i].replace(chr(8211), chr(45))

        print('\nCurrently airing shows : ', *curr_shows, sep='\n')

        name = input('\nEnter name of anime as given in the list above'
                     '\nName : ').replace(chr(8211), chr(45))

        if name not in curr_shows:
            print('This anime cannot be found in the schedule')
            continue

        elif name in shows.keys():
            print('You are already watching this show!')
            continue

        ep = input('Which episode to start downloading from next time you run horrible downloader? ')
        # check if input is valid
        if not ep.isdecimal() or int(ep) < 1:
            print('This is not a valid episode number.')
            continue

        # read the contents of currently watching file
        f = open('horriblefiles/currently_watching.py', 'r')
        cw = f.read()
        f.close()

        # add show to list
        cw = cw.replace('{', '{\n\tr"' + name + '": ' + ep + (',' if len(shows) != 0 else ''))
        shows[name] = int(ep)

        # update the currently watching list
        f = open("horriblefiles/currently_watching.py", "w")
        f.write(cw)
        f.close()

        print('\nAnime added!')

    elif choice == '2':

        print('\nCurrently watching anime :', *shows.keys(), sep='\n')
        
        name = input('\nEnter name of anime as written in list above'
                     '\nName : ').replace(chr(8211), chr(45))

        try:
            # read the contents of currently watching file
            f = open('horriblefiles/currently_watching.py', 'r')
            cw = f.read()
            f.close()

            # remove show from list
            pattern_name = name  # copy of name to be used in the pattern
            for i in special_chars:
                pattern_name = pattern_name.replace(i, '\\' + i)  # add \ to escape special sequence
            cw = re.sub('\n.+"' + pattern_name + '".+,\n', '\n', cw)
            cw = re.sub(',\n.+"' + pattern_name + '".+\n}', '\n}', cw)
            del shows[name]

            # update the currently watching list
            f = open("horriblefiles/currently_watching.py", "w")
            f.write(cw)
            f.close()

        except KeyError:
            print('This anime cannot be found in your currently watching list T-T')

        print('\nAnime removed!')

    elif choice == '3':

        print('\nCurrently watching anime :', *shows.keys(), sep='\n')

        name = input('\nEnter name of anime as written in list above'
                     '\nName : ').replace(chr(8211), chr(45))

        if name not in shows.keys():
            print('This anime cannot be found in your currently watching list T-T')
            continue

        ep = input('Which episode to start downloading from next time you run horrible downloader? ')
        # check if input is valid
        if not ep.isdecimal() or int(ep) < 1:
            print('This is not a valid episode number.')
            continue

        # read the contents of currently watching file
        f = open('horriblefiles/currently_watching.py', 'r')
        cw = f.read()
        f.close()

        # update show in list
        pattern_name = name  # copy of name to be used in the pattern
        for i in special_chars:
            pattern_name = pattern_name.replace(i, '\\' + i)  # add \ to escape special sequence
        cw = re.sub(pattern_name + '": \d+', name + '": ' + ep, cw)

        # update the currently watching list
        f = open("horriblefiles/currently_watching.py", "w")
        f.write(cw)
        f.close()

        print('\nEpisode Updated!')

    elif choice == '4':
        shows.clear()
        # read the contents of currently watching file
        f = open('horriblefiles/currently_watching.py', 'r')
        cw = f.read()
        f.close()

        cw = cw.split('{')[0] + '{\n}\n'

        # update the currently watching list
        f = open("horriblefiles/currently_watching.py", "w")
        f.write(cw)
        f.close()

        print('\nList Cleared!')

    else:
        print('Invalid option. Please try again.')
