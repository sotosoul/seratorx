import platform
import os
from pathlib import Path
import logging
from .constants import SUPPORTED_PLATFORMS, LIBRARY_FOLDER_NAME
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
            library_path: str | Path | None = None,
            logger: logging.Logger | None = None
        ) -> None:
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger
        self.library_path = self.__get_library_path(library_path)

    def __str__(self):
        return f"Seratorx Library <{self.library_path}>"

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

