import logging
from pathlib import Path
from .track import Track
from ..utils import translate_line


class Crate:
    def __init__(
        self,
        path: str | Path,
        logger: logging.Logger | None = None
    ) -> None:

        if logger is None:
            logger = logging.getLogger('Crate')
        self.logger = logger

        if isinstance(path, str):
            path = Path(path)

        self.filepath = path
        filename = path.name

        crate_path_items = filename.split(r'%%')
        crate_item = crate_path_items.pop(-1).replace('.crate', '')

        self.crate_path_items = crate_path_items
        self.crate_item = crate_item

    def __str__(self) -> str:
        return f"< Crate: {self.crate_item} >"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def tracks(self) -> list[str]:

        with open(self.filepath, 'rb') as s:
            s = s.read()
            s = s.replace(b'\n', b'')
            s = s.replace(b'\x00', b'')
            s = s.replace(b'otrk', b'\n')

        lines = s.split(b'\n')

        header = lines.pop(0)  # removes header
        header = header.replace(b'vrsn', b'\nVersion: ')
        self.logger.debug('Header: %s', header)
        self.logger.debug('Total Tracks in Crate %s: %s', self.crate_item, len(lines))

        translated_lines = [translate_line(l) for l in lines]

        return translated_lines

    @property
    def track_count(self) -> int:
        return len(self.tracks)
