import os
import sys

# rootdir = sys.argv
rootdir = '/Users/sotosoul/PycharmProjects/seratorx'

# TODO

for root, subdirs, files in os.walk(rootdir):
    # print(root)
    # print(subdirs)
    print(files)
    # for folder in subdirs:
    #     outfileName = rootdir + '/' + folder + '/py-outfile.txt'  # hardcoded path
    #     folderOut = open( outfileName, 'w' )
    #     print('outfileName is ' + outfileName)
#
#         for file in files:
#             filePath = rootdir + '/' + file
#             f = open( filePath, 'r')
#             toWrite = f.read()
#             print('Writing "' + toWrite + '" to' + filePath)
#             folderOut.write(toWrite)
#             f.close()
#
#         folderOut.close()

