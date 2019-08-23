import io
import os
import shutil
import zipfile
import re

import requests

if input('\nThis will clear your preferences - you will have to setup again.'
         '\nStill want to update? (y/n) - ') != 'y':
    exit(0)

flag_version = "1.1.0"

print('\nDownloading updates...')
r = requests.get('https://github.com/ksdfg/horrible_downloader/releases/latest/download/horrible_downloader.zip',
                 stream=True)
print('Downloaded zip file from the internet.\nExtracting zip file...')
r = zipfile.ZipFile(io.BytesIO(r.content))  # convert file to zip file
r.extractall(os.getcwd())  # extract zip file at given path
print('extracted zip file.')
src = os.getcwd() + r'\horrible_downloader'
dest = os.getcwd()

# check whats the flag version in latest release
fv = ""
with open(r'horrible_downloader\horrible_updater.py', 'r') as f:
    fv = re.compile('\d+\.\d+\.\d+').findall(f.read())

# walk through cwd and replace files with new ones from latest release
for src_dir, dirs, files in os.walk(src):
    dst_dir = src_dir.replace(src, dest, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            # in case no change in structure of currently watching and preferences
            if (file_ == "currently_watching.py" or file_ == "user_preferences.py") and flag_version == fv:
                continue
            os.remove(dst_file)
        shutil.move(src_file, dst_dir)

shutil.rmtree(src)
