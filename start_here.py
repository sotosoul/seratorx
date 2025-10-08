# Use this script as a starting point. Tested on macOS.
# This script does not modify your library, it simply reads
# it but ALWAYS MAKE SURE YOU HAVE UP-TO-DATE BACKUPS FOR
# BOTH YOUR LIBRARY FOLDER (_Serato_) AND THE ACTUAL MUSIC
# FILES (mp3, flac, m4a, wav, etc.)!

import logging
from seratorx import Library

# Set logging level to info so that you don't drown in messages:
logging.basicConfig(level=logging.INFO)

# Initialize your Serato library:
my_library = Library()

# See what this looks like:
print(my_library)

# List your Crates:
my_subcrates = my_library.list_crates()

# List your music files:
my_music_files = my_library.list_music_files()

# List tracks that have been imported to your Library:
my_tracks = my_library.list_tracks(as_dataframe=False)

# List tracks that have been imported to your Library:
my_tracks_in_crates = my_library.list_tracks_in_crates()

# List orphanated Tracks, i.e., tracks that are imported but not in at least one Crate.
my_orphan_tracks = my_library.list_orphans()
print(my_orphan_tracks)
