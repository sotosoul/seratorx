SUPPORTED_PLATFORMS = ['macOS']
EXTENSIONS = ['mp3', 'MP3', 'wav', 'WAV', 'm4a', 'M4A']
LIBRARY_FOLDER_NAME = 'Music'
SRT_TAGS = {
    'vrsn': 'Version',
    'otrk': 'Track',
    'ttyp': 'Type',
    'pfilv': 'Filename',
    'pfil': 'Filename',
    'tsng': 'Song',
    'tart': 'Artist',
    'talb': 'Album',
    'tgen': 'Genre',
    'tlen': 'Length',
    'tcmp': 'Composer',
    'tsiz': 'Size',
    'tbit': 'Bitrate',
    'tsmp': 'Sampling',
    'tbpm': 'BPM',
    'tcom': 'Comment',
    'trmx': 'Remixer',
    'ttyr': 'Year',
    'tadd': 'Date Added',
    'tkey': 'Key',
    'uadd': '',
    'ulbl': '',
    'utme': '',
    'utpc': '',
    'sbav': '',
    'bhrt': '',
    'bmis': '',
    'bply': '',
    'blop': '',
    'bitu': '',
    'bovc': '',
    'bcrt': '',
    'biro': '',
    'bwlb': '',
    'bwll': '',
    'buns': '',
    'bbgl': '',
    'bkrk': '',
    'tlbl': 'Label',
    'utkn': 'Track #',
    'tgrp': 'Grouping',
    'ufsb': '',
    'udsc': '',
    'ptrk': 'Track'
}
ASCII_CONTROL_CHARACTERS = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'    ', b'\x09', b'\x0A', b'\x0B', b'\x0C', b'\x0D', b'\x0E', b'\x0F', b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18', b'\x19', b'\x1A', b'\x1B', b'\x1C', b'\x1D', b'\x1E', b'\x1F', b'\x7F', b'']

SRT_TAGS = [b'ttyp', b'pfilv', b'tsng', b'tart', b'talb', b'tgen', b'tlen', b'tcmp', b'tsiz', b'tbit', b'tsmp', b'tbpm', b'tcom', b'trmx', b'ttyr', b'tadd', b'tkey']

TAGS = [b'\nType: ', b'\nFilename: ', b'\nSong: ', b'\nArtist: ', b'\nAlbum: ', b'\nGenre: ', b'\nLength: ', b'\nComposer: ', b'\nSize: ', b'\nBitrate: ', b'\nSampling: ', b'\nBPM: ', b'\nComment: ', b'\nRemixer: ', b'\nYear: ', b'\nDate Added: ', b'\nKey: ']
