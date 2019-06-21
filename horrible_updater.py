import requests
import zipfile
import io
import os
import shutil

print('\nDownloading updates...')
r = requests.get('https://github.com/ksdfg/horrible_downloader/archive/master.zip', stream=True)
print('Downloaded zip file from the internet.\nExtracting zip file...')
r = zipfile.ZipFile(io.BytesIO(r.content))  # convert file to zip file
r.extractall(os.getcwd())   # extract zip file at given path
print('extracted zip file.')
src = os.getcwd() + r'\horrible_downloader-master'
dest = os.getcwd()

for src_dir, dirs, files in os.walk(src):
    dst_dir = src_dir.replace(src, dest, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            # in case of the src and dst are the same file
            if os.path.samefile(src_file, dst_file):
                continue
            os.remove(dst_file)
        shutil.move(src_file, dst_dir)

shutil.rmtree(src)
