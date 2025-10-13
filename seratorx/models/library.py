import platform
from pathlib import Path
from typing import Any
import logging
from glob import glob
import pandas as pd
from ..models.crate import Crate
from ..models.track import Track
from ..constants import SUPPORTED_PLATFORMS, EXTENSIONS
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

    def __get_directory_path(self, p: str | Path) -> Path:
        if isinstance(p, str):
            p = Path(p)

        p_absolute = p.expanduser().resolve()

        if not p_absolute.exists():
            raise FileNotFoundError(f"Invalid: {p_absolute=}")

        self.logger.info("Directory found: %s", p_absolute)
        return p_absolute

    def __init__(
            self,
            library_database: str | Path = '~/Music/_Serato_/',
            music_files_folder: str | Path | None = '~/Music/Serato/',
            logger: logging.Logger | None = None
        ) -> None:
        """Serato DJ Library instance.

        Your folder containing your music files should have a flat
        hierarchy, meaning *no subfolders*.

        Parameters
        ----------
        library : str | Path, optional
            Path to your Serato library, by default '~/Music/_Serato_/'
        collection : str | Path | None, optional
            Path to the folder containing your music files,
            by default '~/Music/Serato/'
        logger : logging.Logger | None, optional
            Logger, by default None
        """
        if logger is None:
            logger = logging.getLogger('Library')
        self.logger = logger
        self.library = self.__get_directory_path(library_database)
        self.collection = self.__get_directory_path(music_files_folder)

    def __str__(self):
        return f"Serato DJ Library <database: {self.library}, music files: {self.collection}>"

    def __repr__(self):
        return self.__str__()

    @property
    def supported(self):
        return self.__get_os()

    def list_music_files(
        self,
        *,
        full_path: bool = False,
        export_to_txt: bool = False
    ) -> list[str]:
        """Lists music files in your collection folder regardless of
        whether the files have been imported to Serato DJ or not.

        You can optionally export the list as txt file. The filename
        will be `serato_music_files.txt`.

        Parameters
        ----------
        full_path : bool, optional
            Include the full path of the file, by default False

        export_to_txt : bool, optional
            Export to text file, by default False

        Returns
        -------
        list[str]
            _description_
        """

        all_files: list[Path] = []

        for e in EXTENSIONS:
            search_string = f'{self.collection}/*.{e}'
            self.logger.debug(f"Collecting files at {search_string=}")
            paths = glob(search_string)
            self.logger.info(f"Found {len(paths)} {e} files")
            all_files += [Path(p) for p in paths]
        all_files.sort()

        if full_path is True:
            all_files = [str(f) for f in all_files]
        else:
            all_files = [f.name for f in all_files]

        if export_to_txt is True:
            with open('serato_music_files.txt', 'w') as f:
                for file in all_files:
                    f.write(file + "\n")

        return all_files

    def list_crates(self) -> list[Crate]:
        """Lists all your Crates."""

        search_path = f'{self.library.resolve()}/Subcrates/*.crate'

        self.logger.info("Scanning for Crate files: %s", search_path)

        paths = glob(search_path)
        assert paths, f"Missing: {paths=}"

        all_crates = [Path(p) for p in paths]
        all_crates.sort()
        return [Crate(c) for c in all_crates]

    def list_tracks(
        self,
        *,
        as_dataframe: bool = False
    ) -> pd.DataFrame | list[dict[str, Any]]:
        """Lists all the imported Tracks.

        Parameters
        ----------
        as_dataframe : bool, optional
            Return the result as a Pandas Dataframe, by default False

        Returns
        -------
        pd.DataFrame | list[dict]
            Imported Tracks
        """
        database_file_path = self.library / 'database V2'
        self.logger.info("Reading Serato database at: %s", database_file_path)
        return database_reader(database_file_path, as_dataframe)

    def list_tracks_in_crates(
        self,
        *,
        dump_to_file: str | Path | None = None
    ) -> list[str]:
        """Lists all imported Tracks that inside of at least one Crate."""
        tracks_in_crates: list[str] = []
        crates = self.list_crates()

        self.logger.debug("Collecting Tracks from %s Crates...", len(crates))

        for c in crates:
            tracks_in_crates += c.tracks
        tracks_in_crates = list(set(tracks_in_crates))

        self.logger.info("Collected %s unique Tracks from %s (all) Crates.", len(tracks_in_crates), len(crates))

        if dump_to_file:
            self.logger.info("Writing to file: %s", dump_to_file)
            assert isinstance(dump_to_file, (str, Path))
            with open(dump_to_file, 'w') as f:
                for t in tracks_in_crates:
                    f.write(t + '\n')

        return tracks_in_crates

    def list_orphans(self) -> list[str]:
        """Lists tracks that are not in at least one Crate.

        In my opinion, it is important that Tracks are always
        in at least one Crate otherwise they are kind of *lost
        in space*...

        Warning
        -------
        Currently it doesn't work well with non-ascii characters. Working on it.
        """
        orphans = []
        tracks_in_crates = self.list_tracks_in_crates()
        imported_tracks = [t['pfil'] for t in self.list_tracks()]
        imported_tracks_filenames = [t.split('/')[-1] for t in imported_tracks]

        for trk in imported_tracks_filenames:
            self.logger.debug("Checking if `%s` is in at least one Crate...", trk)

            if trk in tracks_in_crates:
                self.logger.debug("Found in Crate: `%s`", trk)
            else:
                self.logger.info("Not in Crate: `%s`", trk)
                orphans.append(trk)

        if orphans:
            self.logger.warning("Found %s orphan (not matched) Tracks", len(orphans))

        return orphans

    def list_nonimported(self) -> set[str]:
        """Lists music files that exist in the respective folder
        but **have not been imported** to the Serato Library."""
        music_files = self.list_music_files()
        tracks = self.list_tracks()
        track_filenames = [trk['pfil'].split('/')[-1] for trk in tracks]
        nonimported = set(music_files) ^ set(track_filenames)  # bitwise or
        # nonimported = set(music_files).difference(track_filenames)  # same as above
        if nonimported:
            self.logger.warning("Found %s non-imported file(s).", len(nonimported))
        return nonimported

    def list_imported(self) -> set[str]:
        """Lists music files that exist in the respective folder
        and **have been imported** to the Serato Library"""
        music_files = self.list_music_files()
        tracks = self.list_tracks()
        track_filenames = [trk['pfil'].split('/')[-1] for trk in tracks]
        imported = set(music_files) & set(track_filenames)  # bitwise and
        # imported = set(music_files).intersection(track_filenames)  # same as above
        if not imported:
            self.logger.error("No files have been imported.")
        else:
            self.logger.info("This many files have been imported: ", len(imported))
        return imported
