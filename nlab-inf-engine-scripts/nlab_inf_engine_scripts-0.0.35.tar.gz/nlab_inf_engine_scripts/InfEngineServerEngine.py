import logging
import re
import shutil
import subprocess
from pathlib import Path

# Paths.
from nlab_inf_engine_scripts.functions import create_dir, symlink

INF_ENGINE_PATH_BIN = "bin/"
INF_ENGINE_PATH_CONF = "conf/"
INF_ENGINE_PATH_LIB = "lib/"
INF_ENGINE_PATH_BUILD = "build/"
INF_ENGINE_PATH_DLDATA = "dldata/"
INF_ENGINE_PATH_DLSOURCES = "sources/"
INF_ENGINE_PATH_ELDATA = "eldata/"
INF_ENGINE_PATH_ELSOURCES = "sources/"

INF_ENGINE_PATH_FUNCTIONS = INF_ENGINE_PATH_LIB + "functions/"

INF_ENGINE_PATH_BUILD_BIN = INF_ENGINE_PATH_BUILD + "bin/"
INF_ENGINE_PATH_BUILD_LIB = INF_ENGINE_PATH_BUILD + "lib/"

# Binaries.
INF_ENGINE_BINARY_COMPILER = INF_ENGINE_PATH_BIN + "InfCompiler"
INF_ENGINE_BINARY_SERVER = INF_ENGINE_PATH_BIN + "InfServer"
INF_ENGINE_BINARY_ELLIPSIS_CMP = INF_ENGINE_PATH_BIN + "EllipsisCompiler"
INF_ENGINE_BINARY_CHECK_SIGNATURE = INF_ENGINE_PATH_BIN + "CheckSignature"
AP_PROCESS_SERVER_BINARY = INF_ENGINE_PATH_BIN + "ap-process-server"

# Binaries sets.
INF_ENGINE_BINARIES_SERVER = [
    AP_PROCESS_SERVER_BINARY,
    INF_ENGINE_PATH_BIN + "InfServer",
    INF_ENGINE_PATH_BIN + "CheckSignature",
]

INF_ENGINE_BINARIES_COMPILERS = [
    INF_ENGINE_PATH_BIN + "InfCompiler",
    INF_ENGINE_PATH_BIN + "EllipsisCompiler",
]
INF_ENGINE_BINARIES_TOOLS = [
    INF_ENGINE_PATH_BIN + "InfServer",
]

# Libraries sets.
INF_ENGINE_LIBRARIES = [
    INF_ENGINE_PATH_LIB + "libClientLib.a",
    INF_ENGINE_PATH_LIB + "libClientLib.dylib",
    INF_ENGINE_PATH_LIB + "libClientLib.so",
]

# Config paths.
INF_ENGINE_CONFIG_FUNCTIONS = INF_ENGINE_PATH_CONF + "functions.lst"

# Files.
INF_ENGINE_FILE_BUILD = "HEAD/InfEngine2/Build.hpp"
INF_ENGINE_FILE_DLDATA = "dldata.ie2"
INF_ENGINE_FILE_ELDATA = "eldata.ie2"
INF_ENGINE_FILE_ALIASES = "aliases.dl"
INF_ENGINE_FILE_ENCODING = "encoding.info"

# Links.
INF_ENGINE_LINK_DLDATA = INF_ENGINE_PATH_DLDATA + "dldata.ie2"
INF_ENGINE_LINK_DLSOURCES = INF_ENGINE_PATH_DLDATA + "dlsources"
INF_ENGINE_LINK_ELDATA = INF_ENGINE_PATH_ELDATA + "eldata.ie2"
INF_ENGINE_LINK_ELSOURCES = INF_ENGINE_PATH_ELDATA + "elsources"
INF_ENGINE_LINK_ALIASES = INF_ENGINE_PATH_DLDATA + "aliases.dl"


class InfEngineServerEngine:
    _engine_dir: Path
    _logger: logging.Logger

    def __init__(self, engine_dir: Path, logger: logging.Logger):
        self._engine_dir = engine_dir

        self._logger = logger

    def check(self, dldata: Path = None):
        """ Check compatibility target DL and/or ellipsis data and InfEngine. """

        if not Path(self._engine_dir / INF_ENGINE_BINARY_CHECK_SIGNATURE).is_file():
            return 0

        cmd = (
            f"{self._engine_dir / INF_ENGINE_BINARY_CHECK_SIGNATURE}"
            f" --inf-server={self._engine_dir / INF_ENGINE_BINARY_SERVER}"
            f" --functions={self._engine_dir / INF_ENGINE_CONFIG_FUNCTIONS}"
            f" --functions-root={self._engine_dir / INF_ENGINE_PATH_FUNCTIONS}"
            f" --base={dldata}"
            f" 2>&1"
        )

        completed_process = subprocess.run(cmd, shell=True)

        return completed_process.returncode

    def compile_dldata(
        self, dlsources: str, configfile: Path, targetfile: Path, strict: bool
    ):
        """ Compile DL date from sources. """

        self._logger.info(f"Compiling DL data: {dlsources}")

        if not Path(self._engine_dir / INF_ENGINE_BINARY_COMPILER).is_file():
            self._logger.error(
                f"Invalid InfCompiler path: {self._engine_dir / INF_ENGINE_BINARY_COMPILER}"
            )
            raise Exception("Invalid InfCompiler path.")

        aliases_file = Path(dlsources) / Path(INF_ENGINE_LINK_ALIASES)
        if not aliases_file.is_file():
            aliases_file = self._engine_dir / Path(INF_ENGINE_LINK_ALIASES)

            if not aliases_file.is_file():
                aliases_file = None

        encoding = ""
        encoding_file = Path(Path(dlsources) / INF_ENGINE_FILE_ENCODING)
        if encoding_file.is_file():
            with encoding_file.open("r") as f:
                source = f.read()

            if re.fullmatch("^UTF(-?)8$", source):
                encoding = "utf-8"
            elif re.fullmatch("^(CP|WIN)(-?)1251$", source):
                encoding = "cp1251"

        cmd = (
            f"{self._engine_dir / INF_ENGINE_BINARY_COMPILER}"
            f" --dldata-root={dlsources}"
            f" --functions-root={self._engine_dir / INF_ENGINE_PATH_FUNCTIONS}"
            f" --target-path={targetfile}"
            f" --strict={'true' if strict else 'false'}"
        )

        if aliases_file:
            cmd += f" --dlaliases {aliases_file}"
        if encoding:
            cmd += f" --encoding {encoding}"

        cmd += f" {configfile} 2>&1"

        self._logger.debug(f"Compiling Dl data: {cmd}")
        completed_process = subprocess.run(cmd, shell=True)

        if completed_process.returncode:
            targetfile.unlink()

            self._logger.error(f"Can't compile DL data: {cmd}")
            raise Exception("Can't compile DL data.")

        self._logger.info(f"DL data compiled.")

    def install(
        self,
        dldata: Path,
        dlsources: Path = None,
        aliases: Path = None,
        db_name: str = "dldata",
    ):
        """ Install DL data to InfEngine. """

        self._logger.info(f"Installing database: {db_name}")

        INF_ENGINE_FILE_DLDATA_VAR = f"{db_name}.ie2"
        INF_ENGINE_LINK_DLDATA_VAR = INF_ENGINE_PATH_DLDATA + INF_ENGINE_FILE_DLDATA_VAR

        dldata_path = create_dir(self._engine_dir / INF_ENGINE_PATH_DLDATA, db_name)

        self._logger.debug(f"dldata_path: {dldata_path}")

        # Install aliases
        if not aliases:
            self._logger.debug(
                f"Aliases were not passed."
                f" Copying {self._engine_dir / INF_ENGINE_LINK_ALIASES}"
                f" to {dldata_path / INF_ENGINE_FILE_ALIASES}"
            )
            if Path(self._engine_dir / INF_ENGINE_LINK_ALIASES).is_file():
                shutil.copy(
                    self._engine_dir / INF_ENGINE_LINK_ALIASES,
                    dldata_path / INF_ENGINE_FILE_ALIASES,
                )
        elif aliases.is_file():
            self._logger.debug(
                f"Aliases were passed."
                f" Copying {aliases}"
                f" to {dldata_path / INF_ENGINE_FILE_ALIASES}"
            )
            shutil.copy(aliases, dldata_path / INF_ENGINE_FILE_ALIASES)
        else:
            raise Exception(f"Invalid aliases path: {aliases}")

        # Install DL data
        if not dldata.is_file():
            raise Exception(f"Invalid DL data path: {dldata}")
        self._logger.debug(
            f"DL data is a file."
            f" Copying {dldata}"
            f" to {dldata_path / INF_ENGINE_FILE_DLDATA_VAR}"
        )
        shutil.copy(dldata, dldata_path / INF_ENGINE_FILE_DLDATA_VAR)

        # Install DL data sources
        if dlsources:
            if not dlsources.is_dir():
                raise Exception(f"Invalid DL data sources path: {dlsources}")
            self._logger.debug(
                f"DL sources is a directory."
                f" Copying {dlsources}"
                f" to {dldata_path / INF_ENGINE_PATH_DLSOURCES}"
            )
            shutil.copytree(dlsources, dldata_path / INF_ENGINE_PATH_DLSOURCES)

            # Install aliases from DL data sources
            sources_aliases = dlsources / INF_ENGINE_FILE_ALIASES

            if not sources_aliases.is_file():
                raise Exception(
                    f"Invalid aliases in DL data sources: {sources_aliases}"
                )

            if not aliases:
                self._logger.debug(
                    f"Copying {sources_aliases}"
                    f" to {dldata_path / INF_ENGINE_FILE_ALIASES}"
                )
                shutil.copy(sources_aliases, dldata_path / INF_ENGINE_FILE_ALIASES)

        # Switching symlinks
        self._logger.debug(
            f"Creating a symlink from {dldata_path / INF_ENGINE_FILE_DLDATA_VAR}"
            f" to {self._engine_dir / (INF_ENGINE_PATH_DLDATA + INF_ENGINE_FILE_DLDATA_VAR)}"
        )
        symlink(
            dldata_path / INF_ENGINE_FILE_DLDATA_VAR,
            self._engine_dir / (INF_ENGINE_PATH_DLDATA + INF_ENGINE_FILE_DLDATA_VAR),
            force=True,
        )

        if db_name == "dldata":
            if Path(dldata_path / INF_ENGINE_PATH_DLSOURCES).is_file():
                self._logger.debug(
                    f"Creating a symlink from {dldata_path / INF_ENGINE_PATH_DLSOURCES}"
                    f" to {self._engine_dir / INF_ENGINE_LINK_DLSOURCES}"
                )
                symlink(
                    dldata_path / INF_ENGINE_PATH_DLSOURCES,
                    self._engine_dir / INF_ENGINE_LINK_DLSOURCES,
                    force=True,
                )
            else:
                self._logger.debug(
                    f"Removing file {self._engine_dir / INF_ENGINE_LINK_DLSOURCES}"
                )
                if Path(self._engine_dir / INF_ENGINE_LINK_DLSOURCES).is_file():
                    Path(self._engine_dir / INF_ENGINE_LINK_DLSOURCES).unlink()

            if Path(dldata_path / INF_ENGINE_FILE_ALIASES).is_file():
                self._logger.debug(
                    f"Creating a symlink from {dldata_path / INF_ENGINE_FILE_ALIASES}"
                    f" to {self._engine_dir / INF_ENGINE_LINK_ALIASES}"
                )
                symlink(
                    dldata_path / INF_ENGINE_FILE_ALIASES,
                    self._engine_dir / INF_ENGINE_LINK_ALIASES,
                    force=True,
                )
            else:
                self._logger.debug(
                    f"Removing file {self._engine_dir / INF_ENGINE_LINK_ALIASES}"
                )
                if Path(self._engine_dir / INF_ENGINE_LINK_DLSOURCES).is_file():
                    Path(self._engine_dir / INF_ENGINE_LINK_DLSOURCES).unlink()

        self.clean(ignore=dldata_path, db_name=db_name)

    def version(self):
        """ Get InfServer version. """

        server = self._engine_dir / INF_ENGINE_BINARY_SERVER

        self._logger.debug(f"Trying to check the server: {server}")

        if server.is_file():
            res = f"{server} --version"

            completed_process = subprocess.run(res, shell=True, stdout=subprocess.PIPE)
            process_stdout = completed_process.stdout.decode("utf-8")

            if completed_process.returncode:
                self._logger.error(f"Can't get InfEngine version: {res}")
                raise Exception(f"Can't get InfEngine version: {res}")
            elif process_stdout.find("Release version:") != -1:
                full_version = re.search(
                    "Release version: ([0-9a-zA-Z.-]+)", process_stdout
                )

                if full_version:
                    version = full_version.group().replace("Release version: ", "")

                    return version

        return None

    def clean(self, ignore: Path, db_name: str, dl_limit: int = 1):
        """ Delete useless data. """

        self._logger.info(f"Cleaning InfServer Engine...")

        count = self._clean_multidb(
            self._engine_dir / INF_ENGINE_PATH_DLDATA, ignore, db_name, dl_limit
        )

        if count:
            self._logger.info(f"Deleted {count} DLData.")

    def _clean_multidb(
        self, directory: Path, ignore: Path, db_name: str, limit: int = 0
    ) -> int:
        """ Delete several DLData directories from the passed directory. """

        counter = 0

        if directory.is_dir():
            for obj in directory.iterdir():
                if limit - counter <= 0:
                    break

                if obj.is_dir() and obj.name.endswith(db_name) and obj != ignore:
                    self._logger.debug(f"Deleting directory: {obj}")
                    shutil.rmtree(obj)

                    counter += 1

        return counter
