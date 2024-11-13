import platform
import os
from pathlib import Path
import logging
from glob import glob
from .constants import SUPPORTED_PLATFORMS, EXTENSIONS
from .exceptions import UnsupportedSystemError


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
            logger = logging.getLogger()
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

    def __get_library_path(self, library_path: str | Path | None) -> Path:
        if library_path is None:
            user_path = os.path.expanduser('~')  # Works on mac & win
            library_path = os.path.join(user_path, LIBRARY_FOLDER_NAME)
        elif isinstance(library_path, (str, Path)):
            pass
        else:
            raise TypeError("Invalid library path: %s, type: %s.",
                            library_path, type(library_path))
        assert os.path.isdir(library_path)
        self.logger.info("Serato library found at %s", library_path)
        return Path(library_path)

    @property
    def supported(self):
        return self.__get_os()

    def get_music_files(self) -> list[Path]:
        # path = path + slash
        # subcrates_full_paths = glob('{}*.crate'.format(path))
        all_files = []
        for e in EXTENSIONS:
            paths = glob(f'{self.collection}/*.{e}')
            all_files += [Path(p) for p in paths]
        all_files.sort()
        return all_files

    def get_crates(self) -> list[Path]:
        # subcrates_full_paths = glob('{}*.crate'.format(path))
        paths = glob(f'{self.library}/Subcrates/*.crate')
        all_crates = [Path(p) for p in paths]
        all_crates.sort()
        return all_crates

    def list_orphans(self):
        """Finds tracks that are not in at least one Crate."""
        ...
