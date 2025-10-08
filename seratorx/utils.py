import os
import shutil
from pathlib import Path
from glob import glob
from datetime import datetime
import pandas as pd
from .constants import ASCII_CONTROL_CHARACTERS, SRT_TAGS, TAGS
import seratorx.constants as constants
import seratorx.decoder as decoder


def get_decoded_string(raw_bytes):
    """Decodes the mixed-encoding byte string to a standard Unicode string."""
    decoded_parts = []
    i = 0
    while i < len(raw_bytes):
        byte1 = raw_bytes[i]
        
        # Two-byte sequence (Greek)
        if byte1 == 0x03 and i + 1 < len(raw_bytes):
            decoded_parts.append(raw_bytes[i:i+2].decode('utf-16-be'))
            i += 2
        # Single-byte sequence (ASCII)
        elif byte1 <= 0x7F:
            decoded_parts.append(chr(byte1))
            i += 1
        else:
            # Fallback for unexpected bytes
            i += 1
            
    return "".join(decoded_parts)


def translate_line(line: str) -> str:
    total_tags = len(SRT_TAGS)
    total_ascii_ctrl_chars = len(ASCII_CONTROL_CHARACTERS)
    for tg in range(0, total_tags):
        for cc in range(0, total_ascii_ctrl_chars):
            tag = SRT_TAGS[tg] + ASCII_CONTROL_CHARACTERS[cc]
            line: bytes = line.replace(tag, TAGS[tg])
    line = line.replace(b'uadd', b'\nUadd (?): ')

    marker = b'Serato/'
    start = line.find(marker)
    utf16_part = line[start + len(marker):]

    track_file = get_decoded_string(utf16_part)

    return track_file



def archive_srt_lib(library_path: Path):
    """
    Creates an archive of the current Serato library directory.
    Works on both mac & windows.
    :return: True of False
    """
    serato_lib_dir = '_Serato_'
    serato_lib_path = os.path.join(library_path, serato_lib_dir)
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    archive_fname = serato_lib_dir + timestamp
    archive_path = os.path.join(library_path, archive_fname)
    shutil.make_archive(archive_path, 'tar', serato_lib_path)
    try:
        os.remove(archive_path + '.tar')
    except:
        pass
    shutil.make_archive(archive_path + '.tar', 'zip', serato_lib_path)
    archived_fname = archive_path + '.tar.zip'
    try:
        prod_fsize = os.path.getsize(archived_fname)
        # print('Serato Library has been archived.\nFilename:{}\nFilesize of archived Serato library:'.format(archived_fname), round(prod_fsize/1000000, 2), 'MB')
        if prod_fsize > 0:
            return True, archive_fname
        else:
            return False, ''
    except FileNotFoundError:
        return False, ''


def convert_unixtime(unix_timestamp):
    if type(unix_timestamp) == str:
        unix_timestamp = int(unix_timestamp)
    dt = datetime.fromtimestamp(unix_timestamp)
    return dt


def str_renamer(str_srt_tag):
    if str_srt_tag in constants.SRT_TAGS:
        return constants.SRT_TAGS[str_srt_tag]
    else:
        return str_srt_tag


def srt_tag_decoder(src_tag):
    if type(src_tag) == str:
        return str_renamer(src_tag)
    elif type(src_tag) is list:
        new_list = []
        for item in src_tag:
            renamed_item = str_renamer(item)
            new_list.append(renamed_item)
        return new_list
    else:
        return src_tag


def database_reader(path, as_dataframe: bool = True) -> pd.DataFrame | list[dict]:
    with open(path, 'rb') as infile:
        data = infile.read()
    decoded_data = decoder.decode(data)
    header = decoded_data.pop(0)
    all_tracks = []
    for track in decoded_data:
        track = dict(track[1])
        all_tracks.append(track)
    if as_dataframe is False:
        return all_tracks
    df = pd.DataFrame(all_tracks).astype(str)
    df.columns = srt_tag_decoder(df.columns.tolist())
    df.fillna('', inplace=True)
    return df


def subcrate_reader(path):
    with open(path, 'rb') as infile:
        data = infile.read()
    decoded_data = decoder.decode(data)
    del decoded_data[0:24]  # First 24 items are not relevant
    all_tracks = []
    for track in decoded_data:
        track = track[1][0][1]
        all_tracks.append(track)
    return all_tracks
    # df = pd.DataFrame(all_tracks)
    # df.columns = srt_tag_decoder(df.columns.tolist())
    # df.fillna('', inplace=True)
    # return df





def df_csv_writer(df, ofname='outfile.csv'):
    df.to_csv(ofname, encoding='utf-8-sig', sep=';')

