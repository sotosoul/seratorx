import os

all_files = []

rootdir = '/Volumes/Music Library/DJ Pool'
for root, subdirs, files in os.walk(rootdir):
    # print(root)
    # print(subdirs)
    print(files)
    # all_files.append(files)


# for file in all_files:
#     print(file)


# print(len(all_files))
