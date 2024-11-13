import seratorx
import os
import sys
import pandas as pd

# Determine working directory
if getattr(sys, 'frozen', False):  # Is application script file or frozen exe?
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
else:
    raise ValueError('Cannot determine working directory!')

os.chdir(application_path)
print('Working directory is: ' + os.getcwd())

current_platform = seratorx.determine_os()





pd.set_option('display.max_columns', 5)

music_path = seratorx.find_music_path()
print(music_path)
main_database_path = os.path.join(music_path, '_Serato_', 'database V2')
subcrates_path = os.path.join(music_path, '_Serato_', 'Subcrates')

my_database = seratorx.database_reader(main_database_path)
my_subcrates = seratorx.subcrates_finder(subcrates_path, current_platform)

print(my_subcrates)
print(my_database)
