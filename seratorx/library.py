import platform
from pathlib import Path
import logging
from .constants import SUPPORTED_PLATFORMS
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
            library_path: str | Path,
            logger: logging.Logger | None = None
        ) -> None:
        if logger is None:
            logger = logging.getLogger()
        self.logger = logger

        self.library_path = library_path

    def __str__(self):
        return f"Seratorx Library <{self.library_path}>"

    def __repr__(self):
        return self.__str__()

    @property
    def supported(self):
        return self.__get_os()

