import os
import platform
import shutil
from datetime import datetime
import seratorx.constants as constants
from glob import glob
import seratorx.decoder as decoder
import pandas as pd


def determine_os():
    """
    Finds whether the system is one of the ones supported by Serato DJ
    I.e., Windows or macOS.
    :return: 'mac' or 'win'
    """
    system = platform.system()
    if system == 'Darwin':
        # version = platform.mac_ver()
        version = 'mac'
    elif system == 'Windows':
        # version = platform.win32_ver()
        version = 'win'
    else:
        raise Exception('Operating System not supported.')
    return version


def find_music_path(music_dir='Music'):
    user_path = os.path.expanduser('~')  # Works on mac & win
    path = os.path.join(user_path, music_dir)
    return path


def archive_srt_lib():
    """
    Creates an archive of the current Serato library directory.
    Works on both mac & windows.
    :return: True of False
    """
    serato_lib_dir = '_Serato_'
    archive_type = 'tar'  # zip or tar. When unZIPped, the size is slightly higher, why???
    path = find_music_path()
    serato_lib_path = os.path.join(path, serato_lib_dir)
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    archive_fname = serato_lib_dir + timestamp
    archive_path = os.path.join(path, archive_fname)
    shutil.make_archive(archive_path, archive_type, serato_lib_path)
    archived_fname = archive_path + '.' + archive_type
    try:
        prod_fsize = os.path.getsize(archived_fname)
        # print('Serato Library has been archived.\nFilename:{}\nFilesize of archived Serato library:'.format(archived_fname), round(prod_fsize/1000000, 2), 'MB')
        if prod_fsize > 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False


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


def subcrates_finder(path, operating_system):
    if operating_system == 'mac':
        path = path + '/'
    elif operating_system == 'win':
        path = path + r'\\'
    subcrates_full_paths = glob('{}*.crate'.format(path))
    subcrate_names = []
    for full_path in subcrates_full_paths:
        subcrate_names.append(full_path)
    subcrate_names.sort()
    return subcrate_names


def database_reader(path):
    with open(path, 'rb') as infile:
        data = infile.read()
    decoded_data = decoder.decode(data)
    header = decoded_data.pop(0)
    all_tracks = []
    for track in decoded_data:
        track = dict(track[1])
        all_tracks.append(track)
    df = pd.DataFrame(all_tracks)
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

