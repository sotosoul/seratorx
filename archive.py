ASCII_CONTROL_CHARACTERS = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'    ', b'\x09', b'\x0A', b'\x0B', b'\x0C', b'\x0D', b'\x0E', b'\x0F', b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18', b'\x19', b'\x1A', b'\x1B', b'\x1C', b'\x1D', b'\x1E', b'\x1F', b'\x7F', b'']

with open(infile, 'rb') as s:
    s = s.read()
    s = s.replace(b'\n', b'')
    s = s.replace(b'\x00', b'')
    s = s.replace(b'otrk', b'\n')

lines = s.split(b'\n')
header = lines.pop(0)  # removes header
header = header.replace(b'vrsn', b'\nVersion: ')
print('Header:', header)
print('Total tracks:', len(lines), '\n')

trackline = lines[986]  # byte
print('SOURCE:\n', trackline, '\n')

SRT_TAGS = [b'ttyp', b'pfilv', b'tsng', b'tart', b'talb', b'tgen', b'tlen', b'tcmp', b'tsiz', b'tbit', b'tsmp', b'tbpm', b'tcom', b'trmx', b'ttyr', b'tadd', b'tkey']

TAGS = [b'\nType: ', b'\nFilename: ', b'\nSong: ', b'\nArtist: ', b'\nAlbum: ', b'\nGenre: ', b'\nLength: ', b'\nComposer: ', b'\nSize: ', b'\nBitrate: ', b'\nSampling: ', b'\nBPM: ', b'\nComment: ', b'\nRemixer: ', b'\nYear: ', b'\nDate Added: ', b'\nKey: ']

total_tags = len(SRT_TAGS)
total_ascii_ctrl_chars = len(ASCII_CONTROL_CHARACTERS)
for tg in range(0, total_tags):
    for cc in range(0, total_ascii_ctrl_chars):
        tag = SRT_TAGS[tg] + ASCII_CONTROL_CHARACTERS[cc]
        trackline = trackline.replace(tag, TAGS[tg])

tracklist = trackline.replace(b'uadd', b'\nUadd (?): ')

tracklist = tracklist.split(b'\n')

for item in tracklist:
    print(item)

# line = lines[0].decode(encoding='ISO-8859-1')




def read_subcrates(path):
    if current_platform == 'mac':
        path = path + '/'
    elif current_platform == 'win':
        path = path + r'\\'
    subcrates_full_paths = glob('{}*.crate'.format(path))
    subcrate_names = []
    for full_path in subcrates_full_paths:
        # full_path = os.path.basename(full_path)
        # full_path = os.path.splitext(full_path)
        # full_path = full_path[0].split('%%')
        subcrate_names.append(full_path)

    subcrate_names.sort()

    # d = {}
    # for crate in subcrate_names:
    #     current_level = d
    #     for part in crate:
    #         if part not in d:
    #             current_level[part] = {}
    #         current_level = current_level[part]
    # print(json.dumps(d))

    return subcrate_names
