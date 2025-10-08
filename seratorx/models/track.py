from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    name: str
    version: str
    track: str
    track_type: str
    filename: str
    song: str
    artist: str
    album: str
    genre: str
    length: str

# {'ttyp': 'mp3', 'pfil': 'Users/sotosoul/Music/Serato/Bro - SydPå.mp3', 'tsng': 'SydPå', 'tart': 'Bro', 'tlen': '03:12.00', 'tsiz': '4.4MB', 'tbit': '192.0kbps', 'tsmp': '44.1k', 'tbpm': '100.00', 'tcom': 'YouTube or soundcloud rips', 'tgrp': 'Danish', 'ttyr': '2018', 'tadd': '1718566184', 'tkey': 'Cm', 'uadd': 1718566184, 'ulbl': 16777215, 'utme': 1527718078, 'ufsb': 4628643, 'utpc': 1, 'sbav': b'\x02\x01', 'bhrt': b'\x01', 'bmis': b'\x00', 'bply': b'\x00', 'blop': b'\x00', 'bitu': b'\x00', 'bovc': b'\x01', 'bcrt': b'\x00', 'biro': b'\x00', 'bwlb': b'\x00', 'bwll': b'\x00', 'buns': b'\x00', 'bbgl': b'\x00', 'bkrk': b'\x00', 'bstm': b'\x00'}