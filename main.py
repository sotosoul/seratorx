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
print(f'MUSIC PATH: {music_path}')
main_database_path = os.path.join(music_path, '_Serato_', 'database V2')
subcrates_path = os.path.join(music_path, '_Serato_', 'Subcrates')
music_files_directory_path = os.path.join(music_path, 'Serato')

my_database = seratorx.database_reader(main_database_path)
my_subcrates = seratorx.subcrates_finder(subcrates_path, current_platform)
tracks_on_disk = seratorx.get_music_files(music_files_directory_path, current_platform)

subcrt_tracks = []
for subcrate in my_subcrates:
    contents = seratorx.subcrate_reader(subcrate)
    subcrt_tracks = subcrt_tracks + contents

subcrt_tracks = set(subcrt_tracks)
subcrt_tracks = list(subcrt_tracks)

if my_database.shape[0] == len(subcrt_tracks):
    print('No orphan tracks found. Total tracks: {}'.format(my_database.shape[0]))
elif my_database.shape[0] > len(subcrt_tracks):
    orphans = my_database.shape[0] - len(subcrt_tracks)
    if orphans == 1:
        s = ''
    else:
        s = 's'
    print('Found {} orphan track{} in your Serato DJ Pro library.'.format(orphans, s))
    print('Database tracks: {}. Tracks in crates: {}'.format(my_database.shape[0], len(subcrt_tracks)))
    database_list = my_database['Filename'].tolist()
    orphan_tracks = list(set(database_list).symmetric_difference(set(subcrt_tracks)))
    print('Orphans:', orphan_tracks)
else:
    raise ValueError('More tracks in crates than in database...?!')

print(f'TOTAL FILES ON DISK: {len(tracks_on_disk)}')
orphan_music_files = list(set(database_list).symmetric_difference(set(tracks_on_disk)))
print(f'ORPHAN FILE ON DISK {len(orphan_music_files)}: {orphan_music_files}')