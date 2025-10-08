import platform
import os
from pathlib import Path
import logging
from glob import glob
import pandas as pd
from ..models.crate import Crate
from ..models.track import Track
from ..constants import SUPPORTED_PLATFORMS, EXTENSIONS, LIBRARY_FOLDER_NAME
from ..exceptions import UnsupportedSystemError
from ..utils import database_reader


class Library:
    def __get_os(self):
        res = {}
        if platform.system() == 'Darwin':
            res['system'] = 'macOS'
            res['version'], _, res['architecture'] = platform.mac_ver()

        if res['system'] in SUPPORTED_PLATFORMS:
            res['supported'] = True
            return res
        else:
            raise UnsupportedSystemError(
                f"Invalid system: {res['system']}. Supported systems: "
                f"{', '.join(SUPPORTED_PLATFORMS)}.")

    def __init__(
            self,
            library: str | Path | None = None,
            collection: str | Path | None = None,
            logger: logging.Logger | None = None
        ) -> None:
        if logger is None:
            logger = logging.getLogger('Library')
        self.logger = logger

        if library is None:
            library = '~/Music/_Serato_/'
            logger.warning("Undefined path of `library`, assuming %s", library)

        self.library = library
        if collection is None:
            collection = '~/Music/Serato/'
            logger.warning("Undefined path of `collection`, assuming: %s", collection)
        self.collection = collection

    def __str__(self):
        return f"Seratorx Library <{self.collection}>"

    def __repr__(self):
        return self.__str__()

    def __get_library_path(self, library_path: str | Path | None = None) -> Path:
        if library_path is None:
            user_path = os.path.expanduser('~')  # Works on mac & win
            library_path = os.path.join(user_path, LIBRARY_FOLDER_NAME)
        elif isinstance(library_path, (str, Path)):
            pass
        else:
            raise TypeError(f"Invalid: {library_path=}, type: {type(library_path)}.")
        assert os.path.isdir(library_path)
        self.logger.info("Serato library found at %s", library_path)
        return Path(library_path)

    @property
    def supported(self):
        return self.__get_os()

    def list_music_files(self, export_to_txt: bool = False) -> list[Path]:
        # path = path + slash
        # subcrates_full_paths = glob('{}*.crate'.format(path))
        all_files: list[Path] = []
        for e in EXTENSIONS:
            search_string = f'{self.collection}/*.{e}'
            self.logger.debug(f"Collecting files at {search_string=}")
            paths = glob(search_string)
            self.logger.info(f"Found {len(paths)} {e} files")
            all_files += [Path(p) for p in paths]
        all_files.sort()
        if export_to_txt is True:
            with open('serato_music_files.txt', 'w') as f:
                for file in all_files:
                    f.write(file.name + "\n")
        return [f.name for f in all_files]

    def list_crates(self) -> list[Crate]:
        # subcrates_full_paths = glob('{}*.crate'.format(path))
        paths = glob(f'{self.library}/Subcrates/*.crate')
        all_crates = [Path(p) for p in paths]
        all_crates.sort()
        return [Crate(c) for c in all_crates]

    def list_tracks(self, as_dataframe: bool = False) -> pd.DataFrame | list[dict]:
        database_file_path = self.__get_library_path() / '_Serato_' / 'database V2'
        self.logger.info("Reading Serato database at: %s", database_file_path)
        return database_reader(database_file_path, as_dataframe)

    def list_orphans(self):
        """Finds tracks that are not in at least one Crate."""
        ...
