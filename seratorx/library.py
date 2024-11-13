import platform
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
