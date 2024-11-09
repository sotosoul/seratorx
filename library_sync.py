import os
from seratorx import file_list
import shutil
import pandas as pd
from time import sleep
from pathlib import Path

# os.system(f"open 'smb://sotosoul:niania@Sotirioss-MacBook-Pro.local/sotosoul/Music' -g")
# sleep(2)  # sec

lib_src = '/Users/sotosoul/Music/test'
lib_dst = '/Users/sotosoul/Desktop/testtete'

if os.path.exists(lib_src):
    print('Found Serato library')

# Load source library
files_src = file_list(lib_src)
files_src = pd.DataFrame.from_dict(files_src)
files_src = files_src[files_src.name != '.DS_Store']

# Load destination library
files_dst = file_list(lib_dst)
files_dst = pd.DataFrame.from_dict(files_src)
files_dst = files_src[files_dst.name != '.DS_Store']

for file in files_src:  # local list
    dst_filepath = os.path.join(lib_dst, file['name'])
    if not os.path.exists(dst_filepath):
        shutil.copy(file['path'], dst_filepath)
        print('copied:', file['path'])
    else:
        print('already exists:', dst_filepath)

    # if file exists in other list
        # if MD5 and filesize same
            # skip


# os.system(f"diskutil unmount /Volumes/Music")
