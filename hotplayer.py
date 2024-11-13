# hotplayer.ru renamer
import os
import sys

URL_CHARS = {
    '%00': '0',
    '%01': '1',
    '%02': '2',
    '%03': '3',
    '%04': '4',
    '%05': '5',
    '%06': '6',
    '%07': '7',
    '%08': '8',
    '%09': '9',
    '%0a': '10',
    '%0b': '11',
    '%0c': '12',
    '%0d': '13',
    '%0e': '14',
    '%0f': '15',
    '%10': '16',
    '%11': '17',
    '%12': '18',
    '%13': '19',
    '%14': '20',
    '%15': '21',
    '%16': '22',
    '%17': '23',
    '%18': '24',
    '%19': '25',
    '%28': '(',
    '%29': ')',
    '%1a': '26',
    '%1b': '27',
    '%1c': '28',
    '%1d': '29',
    '%1e': '30',
    '%1f': '31',
    '%7f': '127',
    '%80': '€',
    '%81': '',
    '%82': '‚',
    '%83': 'ƒ',
    '%84': '„',
    '%85': '…',
    '%86': '†',
    '%87': '‡',
    '%88': 'ˆ',
    '%89': '‰',
    '%8a': 'Š',
    '%8b': '‹',
    '%8c': 'Œ',
    '%8d': '',
    '%8e': 'Ž',
    '%8f': '',
    '%90': '',
    '%91': '‘',
    '%92': '’',
    '%93': '“',
    '%94': '”',
    '%95': '•',
    '%96': '–',
    '%97': '—',
    '%98': '˜',
    '%99': '™',
    '%9a': 'š',
    '%9b': '›',
    '%9c': 'œ',
    '%9d': '',
    '%9e': 'ž',
    '%9f': 'Ÿ',
    '%a0': ' ',
    '%a1': '¡',
    '%a2': '¢',
    '%a3': '£',
    '%a4': '¤',
    '%a5': '¥',
    '%a6': '¦',
    '%a7': '§',
    '%a8': '¨',
    '%a9': '©',
    '%aa': 'ª',
    '%ab': '«',
    '%ac': '¬',
    '%ad': '',
    '%ae': '®',
    '%af': '¯',
    '%b0': '°',
    '%b1': '±',
    '%b2': '²',
    '%b3': '³',
    '%b4': '´',
    '%b5': 'µ',
    '%b6': '¶',
    '%b7': '·',
    '%b8': '¸',
    '%b9': '¹',
    '%ba': 'º',
    '%bb': '»',
    '%bc': '¼',
    '%bd': '½',
    '%be': '¾',
    '%bf': '¿',
    '%c0': 'À',
    '%c1': 'Á',
    '%c2': 'Â',
    '%c3': 'Ã',
    '%c4': 'Ä',
    '%c5': 'Å',
    '%v6': 'Æ',
    '%c7': 'Ç',
    '%c8': 'È',
    '%c9': 'É',
    '%ca': 'Ê',
    '%cb': 'Ë',
    '%cc': 'Ì',
    '%cd': 'Í',
    '%ce': 'Î',
    '%cf': 'Ï',
    '%d0': 'Ð',
    '%d1': 'Ñ',
    '%d2': 'Ò',
    '%d3': 'Ó',
    '%d4': 'Ô',
    '%d5': 'Õ',
    '%d6': 'Ö',
    '%d7': '×',
    '%d8': 'Ø',
    '%d9': 'Ù',
    '%da': 'Ú',
    '%db': 'Û',
    '%dc': 'Ü',
    '%dd': 'Ý',
    '%de': 'Þ',
    '%df': 'ß',
    '%e0': 'à',
    '%e1': 'á',
    '%e2': 'â',
    '%e3': 'ã',
    '%e4': 'ä',
    '%e5': 'å',
    '%e6': 'æ',
    '%e7': 'ç',
    '%e8': 'è',
    '%e9': 'é',
    '%ea': 'ê',
    '%eb': 'ë',
    '%ec': 'ì',
    '%ed': 'í',
    '%ee': 'î',
    '%ef': 'ï',
    '%f0': 'ð',
    '%f1': 'ñ',
    '%f2': 'ò',
    '%f3': 'ó',
    '%f4': 'ô',
    '%f5': 'õ',
    '%f6': 'ö',
    '%f7': '÷',
    '%f8': 'ø',
    '%f9': 'ù',
    '%fa': 'ú',
    '%fb': 'û',
    '%fc': 'ü',
    '%fd': 'ý',
    '%fe': 'þ',
    '%ff': 'ÿ',
    '%24': '$',
    '%26': '&',
    '%27': '\'',
    '%2b': '+',
    '%2c': ',',
    # '%2f': '/',  # Problem with paths
    '%2f': '_',
    '%3a': ':',
    '%3b': ';',
    '%3d': '=',
    '%3f': '?',
    '%40': '@',
    '%20': ' ',
    '%22': '"',
    '%3c': '<',
    '%3e': '>',
    '%23': '#',
    '%25': '%',
    '%7b': '{',
    '%7d': '}',
    '%7c': '|',
    '%5c': '\\',
    '%5e': '^',
    '%7e': '~',
    '%5b': '[',
    '%5d': ']',
    '%60': '`'
}


# Determine working directory
if getattr(sys, 'frozen', False):  # Is application script file or frozen exe?
    working_directory = os.path.dirname(sys.executable)
elif __file__:
    working_directory = os.path.dirname(__file__)
else:
    raise ValueError('Cannot determine working directory!')

os.chdir(working_directory)
print('Working directory is: ' + os.getcwd())

filenames = os.listdir(working_directory)
for file in filenames:
    if file.endswith('.mp3') is True:
        src_filename = os.path.join(working_directory, file)
        for char in URL_CHARS:
            file = file.replace(char, URL_CHARS[char])
        file = file.replace(' (www.hotplayer.ru)', '')  # Optional
        # file = file.replace(' [vk.com/retro_remix]', '')  # Optional
        # file = file.replace(' [vk.com_retro_remix]', '')  # Optional
        dst_filename = os.path.join(working_directory, file)
        if src_filename != dst_filename:
            print(f'Renaming \n{src_filename} \nto \n{dst_filename}\n\n')
            os.rename(src_filename, dst_filename)

