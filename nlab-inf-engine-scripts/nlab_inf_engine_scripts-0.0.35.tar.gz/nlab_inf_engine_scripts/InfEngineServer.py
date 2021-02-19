import logging
import shutil
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path
from time import sleep
from typing import Optional, Union

import memcache

# Paths.
from nlab_inf_engine_scripts.functions import create_dir
from nlab_inf_engine_scripts.InfEngineServerEngine import InfEngineServerEngine

INF_ENGINE_PATH_DATA = "data/"
INF_ENGINE_PATH_TMP = "tmp/"
INF_ENGINE_PATH_CONF = "conf/"
INF_ENGINE_PATH_BIN = "bin/"
INF_ENGINE_PATH_LOGS = "logs/"

INF_ENGINE_PATH_ENGINES = INF_ENGINE_PATH_DATA + "engine"
INF_ENGINE_PATH_RELEASES = INF_ENGINE_PATH_DATA + "release"

# Links.
INF_ENGINE_LINK_READY = "ready"
INF_ENGINE_LINK_RELEASE = "release"

# Filenames.
INF_ENGINE_DLDATA_FILE = "dldata.ie2"
INF_ENGINE_ELDATA_FILE = "eldata.ie2"

# Default root InfEngine server directory.
INF_ENGINE_DEFAULT_ROOT_DIRECTORY = "/usr/local/InfEngine"

# Config paths.
INF_ENGINE_SERVER_CONFIG = INF_ENGINE_PATH_CONF + "InfServer.conf"
AP_PROCESS_SERVER_CONFIG = INF_ENGINE_PATH_CONF + "ap-process-server.conf"
INF_ENGINE_COMPILER_CONFIG = INF_ENGINE_PATH_CONF + "InfCompiler.conf"
INF_ENGINE_ELLIPSIS_COMPILER_CONFIG = INF_ENGINE_PATH_CONF + "EllipsisCompiler.conf"

# Binaries paths.
AP_PROCESS_SERVER_BINARY = INF_ENGINE_PATH_BIN + "ap-process-server"

# Lockfile paths.
INF_ENGINE_LOCK_FILE = INF_ENGINE_PATH_TMP + "BuildEngine.lock"

# Log file.
INF_ENGINE_LOG_FILE_PATH = INF_ENGINE_PATH_LOGS + "InfEngine.log"

# Default memcached server.
DEFAULT_INF_SERVER_CACHE_SERVERS = "localhost:11211"


class InfEngineServer:
    root_path: Path
    _config: dict
    _config_path: dict
    _logger: logging.Logger

    def __init__(
        self,
        root_path: Path = None,
        logging_level: int = logging.ERROR,
        enable_logging: bool = False,
    ):
        """ Class that handles InfEngineServer commands. """

        # Determine the root path
        if root_path:
            self.root_path = Path(root_path)
        else:
            self.root_path = Path(__file__).parent.parent

            if not (
                Path(self.root_path / INF_ENGINE_SERVER_CONFIG).is_file()
                or Path(self.root_path / AP_PROCESS_SERVER_CONFIG).is_file()
                or Path(self.root_path / INF_ENGINE_COMPILER_CONFIG).is_file()
            ):
                self.root_path = Path(INF_ENGINE_DEFAULT_ROOT_DIRECTORY)

        # Create directories
        Path(self.root_path / INF_ENGINE_PATH_TMP).mkdir(exist_ok=True)
        Path(self.root_path / INF_ENGINE_PATH_LOGS).mkdir(exist_ok=True)
        Path(self.root_path / "release" / "dldata").mkdir(exist_ok=True)

        # Create a logger
        self._logger = logging.getLogger("InfEngineServer")
        self._logger.handlers = []

        formatter = logging.Formatter(
            fmt="%(asctime)-30s %(levelname)-10s %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
        )

        log_file_name = Path(self.root_path / INF_ENGINE_LOG_FILE_PATH)
        log_file_name.touch(exist_ok=True)

        handler = logging.FileHandler(
            filename=Path(self.root_path / INF_ENGINE_LOG_FILE_PATH)
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        if enable_logging:
            formatter = logging.Formatter(fmt=" * %(message)s")
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        self._logger.setLevel(logging_level)

        # Config
        self._config = {}
        self._config_path = {}

    def _load_config(
        self, config_type: str, force: bool = False
    ) -> Optional[Union[ConfigParser, dict]]:
        """
        Load InfEngine config.

        :param config_type: Config type. Can be:
         'inf_server',
         'inf_compiler',
         'process_server'
        :param force: Force config re-load if it exists.
        :return: Config dict.
        """

        # Check if config is already loaded
        if not force and config_type in self._config:
            return self._config[config_type]

        self._logger.debug(f"Loading config: {config_type}.")

        # Get config path
        config_path = None

        if config_type == "inf_server":
            config_path = self.root_path / INF_ENGINE_SERVER_CONFIG
        elif config_type == "inf_compiler":
            config_path = self.root_path / INF_ENGINE_COMPILER_CONFIG
        elif config_type == "process_server":
            config_path = self.root_path / AP_PROCESS_SERVER_CONFIG

        self._logger.debug(f"Config path: {config_path}.")

        # Read config
        # TODO: Formatting dependant config parsing. Should change later.
        config = {}
        if config_type in ["inf_server", "inf_compiler"]:
            with Path(config_path).open("r") as f:
                lines = f.read().replace("// ", "#")

            config = ConfigParser()
            config.read_string(lines)

            config = {s: dict(config.items(s)) for s in config.sections()}
        elif config_type == "process_server":
            with Path(config_path).open("r") as f:
                for line in f.readlines():
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue
                    else:
                        key, value = line.split(" ", 1)

                    config[key] = value

        self._logger.debug(f"Config: {config}")

        # Modify values
        if config_type == "inf_server":
            config["Cache"]["servers"] = (
                config["Cache"]["servers"] or DEFAULT_INF_SERVER_CACHE_SERVERS
            ).split(",")
        elif config_type == "inf_compiler":
            pass
        elif config_type == "process_server":
            config["PidFile"] = Path(self.root_path / str(config["PidFile"]))

        self._logger.debug(f"Config: {config}")
        self._config[config_type] = config
        self._config_path[config_type] = config_path

        return config

    def _check(self, pid: int) -> Optional[int]:
        """ Get InfEngine server process info. """

        completed_process = subprocess.run(
            f"ps -p {pid} --no-headers", shell=True, stdout=subprocess.PIPE
        )

        self._logger.debug(f"Process: {completed_process.stdout}")

        if completed_process.stdout:
            return pid
        else:
            return None

    def _pid(self) -> Optional[int]:
        """ Get InfEngine server pid. """

        config = self._load_config("process_server")

        pidfile = Path(config["PidFile"])

        self._logger.debug(f"Pid file path: {pidfile}")

        if not pidfile.is_file():
            return None

        self._logger.debug(f"Pid file exists.")

        try:
            with pidfile.open("r") as f:
                pid = f.read().strip()
        except Exception as e:
            self._logger.error(f"Can't open pidfile '{pidfile}': {e}")

            raise e

        if not pid:
            return None
        else:
            try:
                pid = int(pid)
            except Exception as e:
                self._logger.error(
                    f"Invalid InfEngine server pid file '{pidfile}': {pid}"
                )

        self._logger.debug(f"Pid: {pid}.")

        return self._check(pid)

    def start(self):
        """ Start InfEngine server. """

        self._logger.info("Starting InfEngine server.")

        if self._pid():
            self._logger.warning("Can't start InfEngine server: it is already running.")
            return

        self._load_config("process_server")

        res = f"cd '{self.root_path}' && {self.root_path / AP_PROCESS_SERVER_BINARY} {self._config_path['process_server']} 2>&1"

        config = self._load_config("inf_server")

        self._logger.debug("Flushing Memcached servers.")
        memcache.Client(servers=config["Cache"]["servers"]).flush_all()

        try:
            self._logger.debug(f"Trying to start the server: {res}")
            completed_process = subprocess.run(res, shell=True)
        except subprocess.TimeoutExpired as e:
            self._logger.error("Can't start InfEngine server: timeout is expired.")
            raise Exception(f"Can't start InfEngine server: timeout is expired.")
        else:
            if completed_process.returncode != 0:
                self._logger.error(
                    f"Can't start InfEngine server: {res}, {completed_process.returncode}"
                )
                raise Exception(
                    f"Can't start InfEngine server: {res}, {completed_process.returncode}"
                )

        # Sleep until the server is started
        while True:
            if not self._pid():
                sleep(1)
            else:
                break

        self._logger.info("InfEngine server has started.")

    def stop(self):
        """ Stop InfEngine server. """

        self._logger.info("Stopping InfEngine server.")

        pid = self._pid()
        if not pid:
            self._logger.warning("Can't stop InfEngine server: it isn't running.")
            return

        # Try to kill the process
        res = f"kill -TERM {pid}"

        try:
            self._logger.debug(f"Trying to kill the server: {res}")
            completed_process = subprocess.run(res, shell=True)
        except subprocess.TimeoutExpired as e:
            self._logger.error("Can't kill InfEngine server: timeout is expired.")
            return
        else:
            if completed_process.returncode != 0:
                self._logger.error(f"Can't stop InfEngine server: {res}")
                return

        # Sleep until the server is stopped
        while True:
            if self._check(pid):
                sleep(1)
            else:
                break

        self._logger.info("InfEngine server has stopped.")

    def restart(self):
        """ Restart InfEngine server. """

        self._logger.info("Restarting InfEngine server.")

        if self._pid():
            self.stop()

            sleep(5)

            self.start()
        else:
            self._logger.warning("Can't restart InfEngine server: it isn't running.")

    def respawn(self):
        """ Respawn InfEngine workers. """

        self._logger.info("Respawning InfEngine workers.")

        pid = self._pid()
        if not pid:
            self._logger.warning(
                "Can't respawn InfEngine workers: server wasn't started."
            )
            return

        res = f"kill -HUP {pid}"

        try:
            self._logger.debug(f"Trying to kill the server: {res}")
            completed_process = subprocess.run(res, shell=True)
        except subprocess.TimeoutExpired as e:
            self._logger.error("Can't kill InfEngine server: timeout is expired.")
            return
        else:
            if completed_process.returncode != 0:
                self._logger.error(f"Can't stop InfEngine server: {res}")
                return

        sleep(10)

        self._logger.info("InfEngine workers have respawned.")

    def status(self):
        """ Check InfEngine server status. """

        if self._pid():
            return "RUNNING"
        else:
            return "NOT RUNNING"

    def update_data(
        self,
        dldata: str = None,
        dlsources: str = None,
        strict: bool = False,
        db_name: str = "dldata",
    ):
        """ Update DL data. """

        self._logger.info("Updating Data.")

        if Path(dldata).is_file():
            dldata = Path(dldata)

            self._logger.info(f"DL data path: {dldata}")
        elif Path(dldata).is_dir():
            dlsources = Path(dldata)
            dldata = None

            self._logger.info(f"DL sources path: {dlsources}")
        else:
            self._logger.error(f"Invalid path: {dldata}")
            raise Exception(f"Invalid path: {dldata}")

        # TODO: lock

        engine = InfEngineServerEngine(
            self.root_path / INF_ENGINE_LINK_RELEASE, logger=self._logger
        )

        temp_dir_path = create_dir(
            self.root_path / INF_ENGINE_PATH_TMP, db_name=db_name
        )
        self._logger.debug(f"Creating a dir: {temp_dir_path}.")

        if dldata:
            if engine.check(dldata) == 0:
                self._logger.info(f"Updating DL data binary: {dldata}")
            else:
                self._logger.error(f"DL data is incompatible.")
                raise Exception(f"DL data is incompatible.")
        elif dlsources:
            self._logger.info(f"Updating DL data from sources: {dlsources}")

            dldata = temp_dir_path / INF_ENGINE_DLDATA_FILE
            engine.compile_dldata(
                dlsources, self.root_path / INF_ENGINE_COMPILER_CONFIG, dldata, strict
            )

        engine.install(dldata, dlsources, db_name=db_name)

        shutil.rmtree(temp_dir_path)
        self.respawn()

    def delete_dl(self, database_name):
        """ Delete DL databases. """

        file = (
            self.root_path / INF_ENGINE_LINK_RELEASE / "dldata" / f"{database_name}.ie2"
        )

        self._logger.info(f"Deleting database: {file}")

        file.unlink()

    def delete_dl_all(self):
        """ Delete DL databases. """

        directory = self.root_path / INF_ENGINE_LINK_RELEASE / "dldata"

        self._logger.info(f"Deleting all databases from: {directory}")

        for obj in directory.iterdir():
            self._logger.debug(f"Deleting: {obj}")
            if obj.is_file():
                obj.unlink()
            elif obj.is_dir():
                shutil.rmtree(obj)

    def version(self):
        """ Get InfServer version. """

        engine = InfEngineServerEngine(
            self.root_path / INF_ENGINE_LINK_RELEASE, logger=self._logger
        )

        return engine.version()
