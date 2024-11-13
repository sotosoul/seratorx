from seratorx import Library

lib = Library(
    library='/Users/sotosoul/Library/Mobile Documents/com~apple~CloudDocs/Music/_Serato_/',
    collection='/Users/sotosoul/Library/Mobile Documents/com~apple~CloudDocs/Music/Serato/'
)

files = lib.get_music_files()
for f in files[0:2]:
    # print(f)
    pass
print("Total music files:", len(files))

crates = lib.get_crates()
for c in crates[0:2]:
    print(c)
    pass
print("Total crates:", len(crates))
