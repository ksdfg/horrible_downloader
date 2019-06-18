# python script to update your currently watching list
from horriblefiles.currently_watching import shows
from bs4 import BeautifulSoup as bs
import requests
import re

# get a list of ALL currently airing shows
# make sure iDOLM@STER doesn't get replaced by [email protected]
curr_shows = list(map(lambda x: x.text.replace('[email protected]', 'iDOLM@STER'),
                      bs(requests.get("https://horriblesubs.info/release-schedule/").text,
                         features='html.parser').select('a[title = "See all releases for this show"]')
                      ))

special_chars = ['+', '*', '.', '|', '(', ')', '$', '{', '}', '[', ']']  # set of all special chars in patterns

# interactive loop
while True:
    print('\n1. Add anime to currently watching list\t(type 1 to select this)'
          '\n2. Remove anime from currently watching\t(type 2 to select this)'
          '\n3. Change next episode to download of anime in currently watching list\t(type 3 to select this)'
          '\n4. Exit\t(type 4 to select this)')     # printing options
    choice = input('Choice : ')

    if choice == '4':   # user wants to exit
        break

    elif choice == '1':     # user wants to add anime to list

        name = input('\nEnter name of anime as written in the schedule of horriblesubs.info'
                     '\nLink to schedule - https://horriblesubs.info/release-schedule/'
                     '\nName : ')

        if name not in curr_shows:
            print('This anime cannot be found in the schedule')
            continue

        elif name in shows.keys():
            print('You are already watching this show!')
            continue

        ep = input('Which episode to download next time you run horrible downloader? ')
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

    elif choice == '2':
        name = input('\nEnter name of anime as written in the schedule of horriblesubs.info'
                     '\nLink to schedule - https://horriblesubs.info/release-schedule/'
                     '\nName : ')

        try:
            # read the contents of currently watching file
            f = open('horriblefiles/currently_watching.py', 'r')
            cw = f.read()
            f.close()

            # remove show from list
            pattern_name = name     # copy of name to be used in the pattern
            for i in special_chars:
                pattern_name = pattern_name.replace(i, '\\'+i)      # add \ to escape special sequence
            cw = re.sub('\n.+"' + pattern_name + '".+\n', '\n', cw)
            del shows[name]

            # update the currently watching list
            f = open("horriblefiles/currently_watching.py", "w")
            f.write(cw)
            f.close()

        except KeyError:
            print('This anime cannot be found in your currently watching list T-T')

    elif choice == '3':
        name = input('\nEnter name of anime as written in the schedule of horriblesubs.info'
                     '\nLink to schedule - https://horriblesubs.info/release-schedule/'
                     '\nName : ')

        if name not in shows.keys():
            print('This anime cannot be found in your currently watching list T-T')
            continue

        ep = input('Which episode to download next time you run horrible downloader? ')
        # check if input is valid
        if not ep.isdecimal() or int(ep) < 1:
            print('This is not a valid episode number.')
            continue

        # read the contents of currently watching file
        f = open('horriblefiles/currently_watching.py', 'r')
        cw = f.read()
        f.close()

        # update show in list
        pattern_name = name     # copy of name to be used in the pattern
        for i in special_chars:
            pattern_name = pattern_name.replace(i, '\\'+i)      # add \ to escape special sequence
        cw = re.sub(pattern_name + '": \d+', name + '": ' + ep, cw)

        # update the currently watching list
        f = open("horriblefiles/currently_watching.py", "w")
        f.write(cw)
        f.close()

    else:
        print('Invalid option. Please try again.')
