import hashlib
import inspect
import json
import os
import subprocess
import sys
import tempfile
import time
from typing import Any, cast, Dict, List, Optional, Tuple, Union

import colorama  # type: ignore
import ray
import ray.autoscaler.sdk
import requests
import yaml

from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.credentials import load_credentials
from anyscale.fingerprint import fingerprint
import anyscale.project
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK  # type: ignore

# The default project directory to use, if no project is specified.
DEFAULT_SCRATCH_DIR = "~/.anyscale/scratch_project"

# The key used to identify the session's latest file hash.
ANYSCALE_FILES_HASH = "anyscale.com/local_files_hash"

# Max number of auto created sessions.
MAX_SESSIONS = 20

# Default minutes for autosuspend.
DEFAULT_AUTOSUSPEND_TIMEOUT = 120


# Default docker images to use for connect sessions.
def _get_base_image(cpu_or_gpu: str = "cpu") -> str:
    py_version = "".join(str(x) for x in sys.version_info[0:2])
    if py_version not in ["36", "37", "38"]:
        raise ValueError("No default docker image for py{}".format(py_version))
    return "anyscale/ray-ml:nightly-py{}-{}".format(py_version, cpu_or_gpu)


class _ConsoleLog:
    def __init__(self) -> None:
        self.t0 = time.time()

    def zero_time(self) -> None:
        self.t0 = time.time()

    def info(self, *msg: Any) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.BRIGHT,
                colorama.Fore.CYAN,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def debug(self, *msg: str) -> None:
        if os.environ.get("DEBUG") == "1":
            print(
                "{}{}(anyscale +{}){} ".format(
                    colorama.Style.DIM,
                    colorama.Fore.CYAN,
                    self._time_string(),
                    colorama.Style.RESET_ALL,
                ),
                end="",
            )
            print(*msg)

    def error(self, *msg: str) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.BRIGHT,
                colorama.Fore.RED,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def _time_string(self) -> str:
        delta = time.time() - self.t0
        hours = 0
        minutes = 0
        while delta > 3600:
            hours += 1
            delta -= 3600
        while delta > 60:
            minutes += 1
            delta -= 60
        output = ""
        if hours:
            output += "{}h".format(hours)
        if minutes:
            output += "{}m".format(minutes)
        output += "{}s".format(round(delta, 1))
        return output


class SessionBuilder:
    """This class lets you set session options and connect to Anyscale.

    This feature is ***EXPERIMENTAL***.

    It should not be constructed directly, but instead via anyscale.* methods
    exported at the package level.

    Examples:
        >>> # Raw client, creates new session on behalf of user
        >>> anyscale.connect()

        >>> # Get or create a named session
        >>> anyscale
        ...   .session("my_named_session")
        ...   .connect()

        >>> # Specify a previously created env / app template
        >>> anyscale
        ...   .app_env("prev_created_env:v2")
        ...   .autosuspend(hours=2)
        ...   .connect()

        >>> # Create new session from local env / from scratch
        >>> anyscale
        ...   .project_dir("~/dev/my-project-folder")
        ...   .base_docker_image("anyscale/ray-ml:nightly")
        ...   .require("~/dev/my-project-folder/requirements.txt")
        ...   .connect()

        >>> # Ray client connect is setup automatically
        >>> @ray.remote
        ... def my_func(value):
        ...   return value ** 2

        >>> # Remote functions are executed in the Anyscale session
        >>> print(ray.get([my_func.remote(x) for x in range(5)]))
        >>> [0, 1, 4, 9, 16]
    """

    def __init__(
        self,
        scratch_dir: str = DEFAULT_SCRATCH_DIR,
        anyscale_sdk: AnyscaleSDK = None,
        subprocess: Any = subprocess,
        requests: Any = requests,
        ray: Any = ray,
        log: Any = _ConsoleLog(),
    ) -> None:
        # Class dependencies.
        self._log = log
        self._anyscale_sdk: Any = None
        if anyscale_sdk:
            self._anyscale_sdk = anyscale_sdk
        else:
            credentials = load_credentials()
            self._log.debug("Using host {}".format(anyscale.conf.ANYSCALE_HOST))
            self._log.debug("Using credentials {}".format(credentials))
            self._anyscale_sdk = AnyscaleSDK(
                credentials, os.path.join(anyscale.conf.ANYSCALE_HOST, "ext")
            )
        self._ray: Any = ray
        self._subprocess: Any = subprocess
        self._requests: Any = requests

        # Builder args.
        self._scratch_dir: str = scratch_dir
        self._ray_release: Optional[str] = None
        self._project_dir: Optional[str] = None
        self._cloud_name: Optional[str] = None
        self._session_name: Optional[str] = None
        self._base_docker_image: Optional[str] = None
        self._requirements: Optional[str] = None
        self._initial_scale: List[Dict[str, float]] = []
        self._autosuspend_timeout = DEFAULT_AUTOSUSPEND_TIMEOUT

        # Whether to update the session when connecting to a fixed session.
        self._needs_update: bool = True

        # A temporary connection to use to lock the right session.
        self._tmp_conn: Any = None

    def connect(self) -> None:
        """Connect to Anyscale using previously specified options.

        Examples:
            >>> anyscale.connect()
        """

        # TODO(ekl) check for duplicate connections
        self._log.zero_time()

        if ray.util.client.ray.is_connected():
            raise RuntimeError(
                "Already connected to a Ray session, please "
                "run anyscale.connect in a new Python process."
            )

        # Allow the script to be run on the head node as well.
        if "ANYSCALE_SESSION_ID" in os.environ:
            self._log.info("Running in remote Anyscale session.")
            ray.init(address="auto")
            return

        # Autodetect or create a scratch project.
        if self._project_dir is None:
            self._project_dir = anyscale.project.find_project_root(os.getcwd())
        if self._project_dir:
            self._ensure_project_setup_at_dir(self._project_dir)
        else:
            self._project_dir = self._get_or_create_scratch_project()
        proj_def = anyscale.project.ProjectDefinition(self._project_dir)
        project_id = anyscale.project.get_project_id(proj_def.root)
        self._log.info("Using project dir", proj_def.root)

        # TODO(ekl): generate a serverless compute configuraton here.
        cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
        self._populate_cluster_config(
            cluster_yaml, self._anyscale_sdk.get_project(project_id).result.name
        )
        with open(os.path.join(self._project_dir, "session-default.yaml"), "w+") as f:
            f.write(yaml.dump(cluster_yaml))

        # Run finger printing after session-default.yaml is written so it is part
        # of the finger print.
        files_hash = self._fingerprint(proj_def.root)

        if self._session_name is not None:
            sess = self._get_session(project_id, self._session_name)
            if not sess or sess.state != "Running":
                # Unconditionally create the session if it isn't up.
                needs_up = True
            else:
                needs_up = self._needs_update
        else:
            needs_up = False

        # Locate a updated session and update it if needed.
        if self._session_name is None or needs_up:
            self._session_name = self._get_or_create_updated_session(
                files_hash.encode("utf-8"), project_id, self._session_name
            )

        # Connect Ray client.
        self._connect_to_session(project_id, self._session_name)

        # Issue request resources call.
        if self._initial_scale:
            self._log.debug("Calling request_resources({})".format(self._initial_scale))
            ray.autoscaler.sdk.request_resources(bundles=self._initial_scale)

        # Can release the session lock now that we are connected for real.
        if self._tmp_conn:
            self._tmp_conn.disconnect()
            self._tmp_conn = None

        # Define ray in the notebook automatically for convenience.
        try:
            fr: Any = inspect.getouterframes(inspect.currentframe())[-1]
            if fr.filename == "<stdin>" and "ray" not in fr.frame.f_globals:
                self._log.debug("Auto importing Ray into the notebook.")
                fr.frame.f_globals["ray"] = ray
        except Exception as e:
            self._log.error("Failed to auto define `ray` in notebook", e)

    def cloud(self, cloud_name: str) -> "SessionBuilder":
        """Set the name of the cloud to be used.

        This sets the name of the cloud that your connect session will be
        started in. If you do not specify it, it will use the last used cloud
        in this project.

        Args:
            cloud_name (str): Name of the cloud to start the session in.

        Examples:
            >>> anyscale.cloud("aws_test_account").connect()
        """
        self._cloud_name = cloud_name
        return self

    def project_dir(self, local_dir: str) -> "SessionBuilder":
        """Set the project directory.

        This sets the project code directory that will be synced to all nodes
        in the cluster as required by Ray. If not specified, the project
        directory will be autodetected based on the current working directory.
        If no Anyscale project is found, a "scratch" project will be used.

        Args:
            local_dir (str): path to the project directory.

        Examples:
            >>> anyscale.project_dir("~/my-proj-dir").connect()
        """
        self._project_dir = os.path.abspath(os.path.expanduser(local_dir))
        return self

    def session(self, session_name: str, update: bool = False) -> "SessionBuilder":
        """Set a fixed session name.

        By default, Anyscale connect will pick an idle session updated
        with the connect parameters, creating a new session if no updated
        idle sessions. Setting a fixed session name will force connecting to
        the given named session, creating it if it doesn't exist.

        Args:
            session_name (str): fixed name of the session.
            update (bool): whether to update session configurations when
                connecting to an existing session. Note that this may restart
                the Ray runtime.

        Examples:
            >>> anyscale.session("prod_deployment", update=True).connect()
        """
        if not update:
            self._needs_update = False
        self._session_name = session_name
        return self

    def base_docker_image(self, image_name: str) -> "SessionBuilder":
        """Set the docker image to use for the session.

        Args:
            image_name (str): docker image name.

        Examples:
            >>> anyscale.base_docker_image("anyscale/ray-ml:latest").connect()
        """
        self._base_docker_image = image_name
        return self

    def require(self, requirements: Union[str, List[str]]) -> "SessionBuilder":
        """Set the Python requirements for the session.

        Args:
            requirements: either be a list of pip library specifications, or
            the path to a requirements.txt file.

        Examples:
            >>> anyscale.require("~/proj/requirements.txt").connect()
            >>> anyscale.require(["gym", "torch>=1.4.0"]).connect()
        """
        if isinstance(requirements, str):
            with open(requirements, "r") as f:
                data = f.read()
            # Escape quotes
            self._requirements = data.replace('"', r"\"")
        else:
            assert isinstance(requirements, list)
            self._requirements = "\n".join(requirements)
        return self

    def app_env(self, env_name: str) -> "SessionBuilder":
        """Set the Anyscale app env to use for the session.

        Args:
            env_name (str): app env name.

        Examples:
            >>> anyscale.app_env("prev_created_env:v2").connect()
        """
        raise NotImplementedError()

    def file_mount(self, *, local_dir: str, remote_dir: str) -> "SessionBuilder":
        """Add additional directories to sync up to worker nodes.

        Args:
            local_dir (str): the local directory path to mount.
            remote_dir (str): where in the remote node to mount the local dir.

        Examples:
            >>> anyscale
            ...   .file_mount(local_dir="~/data1", remote_dir="/tmp/d1")
            ...   .file_mount(local_dir="~/data2", remote_dir="/tmp/d2")
            ...   .connect()
        """
        raise NotImplementedError()

    def download_results(
        self, *, remote_dir: str, local_dir: str, autosync: bool = False
    ) -> "SessionBuilder":
        """Specify a directory to sync down from the cluster head node.

        Args:
            remote_dir (str): the remote result dir on the head node.
            local_dir (str): the local path to sync results to.
            autosync (bool): whether to sync the files continuously. By
                default, results will only be synced on job completion.

        Examples:
            >>> anyscale
            ...   .download_results(
            ...       remote_dir="~/ray_results", remote_dir="~/proj_output",
            ...       autosync=True)
            ...   .connect()
        """
        raise NotImplementedError()

    def autosuspend(
        self,
        enabled: bool = True,
        *,
        hours: Optional[int] = None,
        minutes: Optional[int] = None,
    ) -> "SessionBuilder":
        """Configure or disable session autosuspend behavior.

        The session will be autosuspend after the specified time period. By
        default, sessions auto terminate after one hour of idle.

        Args:
            enabled (bool): whether autosuspend is enabled.
            hours (int): specify idle time in hours.
            minutes (int): specify idle time in minutes. This is added to the
                idle time in hours.

        Examples:
            >>> anyscale.autosuspend(False).connect()
            >>> anyscale.autosuspend(hours=10).connect()
            >>> anyscale.autosuspend(hours=1, minutes=30).connect()
        """
        if enabled:
            if hours is None and minutes is None:
                timeout = DEFAULT_AUTOSUSPEND_TIMEOUT
            else:
                timeout = 0
                if hours is not None:
                    timeout += hours * 60
                if minutes is not None:
                    timeout += minutes
        else:
            timeout = -1
        self._autosuspend_timeout = timeout
        return self

    def nightly_build(self, git_commit: str) -> "SessionBuilder":
        """Use the specified nightly build commit for the session runtime.

        Args:
            git_commit (str): git commit of the nightly Ray release.

        Examples:
            >>> anyscale
            ...   .nightly_build("f1e293c6997d1b14d61b8ca05965af42ae59d285")
            ...   .connect()
        """
        if len(git_commit) != 40:
            raise ValueError("Ray git commit hash must be 40 chars long")
        self._ray_release = "master/{}".format(git_commit)
        url = self._get_wheel_url(self._ray_release)
        request = self._requests.head(url)
        if request.status_code != 200:
            raise ValueError(
                "Could not locate wheel in S3 (HTTP {}): {}".format(
                    request.status_code, url
                )
            )
        return self

    def initial_scale(
        self,
        *,
        num_cpus: Optional[int] = None,
        num_gpus: Optional[int] = None,
        bundles: Optional[List[Dict[str, float]]] = None,
    ) -> "SessionBuilder":
        """Configure the initial resources to scale to.

        The session will immediately attempt to scale to accomodate the
        requested resources, bypassing normal upscaling speed constraints.
        The requested resources are pinned and exempt from downscaling.

        Args:
            num_cpus (int): number of cpus to request.
            num_gpus (int): number of gpus to request.
            bundles (List[Dict[str, float]): resource bundles to
                request. Each bundle is a dict of resource_name to quantity
                that can be allocated on a single machine. Note that the
                ``num_cpus`` and ``num_gpus`` args simply desugar into
                ``[{"CPU": 1}] * num_cpus`` and ``[{"GPU": 1}] * num_gpus``
                respectively.

        Examples:
            >>> anyscale.initial_scale(num_cpus=200, num_gpus=30).connect()
            >>> anyscale.initial_scale(
            ...     num_cpus=8,
            ...     resource_bundles=[{"GPU": 8}, {"GPU": 8}, {"GPU": 1}],
            ... ).connect()
        """
        to_request: List[Dict[str, float]] = []
        if num_cpus:
            to_request += [{"CPU": 1}] * num_cpus
        if num_gpus:
            to_request += [{"GPU": 1}] * num_gpus
        if bundles:
            to_request += bundles
        self._initial_scale = to_request
        return self

    def _get_or_create_scratch_project(self) -> str:
        """Get or create a scratch project, including the directory."""
        project_dir = os.path.expanduser(self._scratch_dir)
        project_name = os.path.basename(self._scratch_dir)
        if not os.path.exists(project_dir) and self._project_exists(project_name):
            self._clone_project(project_dir, project_name)
        else:
            self._ensure_project_setup_at_dir(project_dir)
        return project_dir

    def _project_exists(self, project_name: str) -> bool:
        """Return if a project of a given name exists."""
        resp = self._anyscale_sdk.search_projects({"name": {"equals": project_name}})
        return len(resp.results) > 0

    def _clone_project(self, project_dir: str, project_name: str) -> None:
        """Clone a project into the given dir by name."""
        cur_dir = os.getcwd()
        try:
            parent_dir = os.path.dirname(project_dir)
            os.makedirs(parent_dir, exist_ok=True)
            os.chdir(parent_dir)
            self._subprocess.check_call(["anyscale", "clone", project_name])
        finally:
            os.chdir(cur_dir)

    def _ensure_project_setup_at_dir(self, project_dir: str) -> None:
        """Get or create an Anyscale project rooted at the given dir."""
        os.makedirs(project_dir, exist_ok=True)
        proj_name = os.path.basename(project_dir)

        # If the project yaml exists, assume we're already setup.
        project_yaml = os.path.join(project_dir, ".anyscale.yaml")
        if os.path.exists(project_yaml):
            return

        self._log.info("Creating new project for", project_dir)
        project_response = self._anyscale_sdk.create_project(
            {
                "name": proj_name,
                "description": "Automatically created by Anyscale Connect",
            }
        )
        project_id = project_response.result.id

        if not os.path.exists(project_yaml):
            with open(project_yaml, "w+") as f:
                f.write(yaml.dump({"project_id": project_id}))

    def _up_session(
        self, project_id: str, session_name: str, cloud_name: str, cwd: Optional[str]
    ) -> None:
        # Non-blocking version of check_call, see
        # https://github.com/python/cpython/blob/64abf373444944a240274a9b6d66d1cb01ecfcdd/Lib/subprocess.py#L363
        command = [
            "anyscale",
            "up",
            "--idle-timeout",
            str(self._autosuspend_timeout),
            "--config",
            "session-default.yaml",
            "--cloud-name",
            cloud_name,
            session_name,
        ]
        with tempfile.NamedTemporaryFile(delete=False) as output_log_file:
            with self._subprocess.Popen(
                command, cwd=cwd, stdout=output_log_file, stderr=subprocess.STDOUT,
            ) as p:
                # Get session URL:
                session_found = False
                retry_time = 1.0
                while not session_found and retry_time < 10:
                    results = self._list_sessions(project_id=project_id)
                    for session in results:
                        if session.name == session_name:
                            self._log.info(
                                "Updating session, see: {}/o/anyscale-internal/"
                                "projects/{}/sessions/{}".format(
                                    anyscale.conf.ANYSCALE_HOST, project_id, session.id
                                )
                            )
                            session_found = True
                    time.sleep(retry_time)
                    retry_time = 2 * retry_time
                try:
                    retcode = p.wait()
                except Exception as e:
                    p.kill()
                    raise e
                # Check for errors:
                if retcode:
                    cmd = " ".join(command)
                    msg = "Executing '{}' in {} failed.".format(cmd, self._project_dir)
                    self._log.error(
                        "--------------- Start update logs ---------------\n"
                        "{}".format(open(output_log_file.name).read())
                    )
                    self._log.error("--------------- End update logs ---------------")
                    raise RuntimeError(msg)

    def _get_last_used_cloud(self, project_id: str) -> str:
        """Return the name of the cloud last used in the project.

        Args:
            project_id (str): The project to get the last used cloud for.

        Returns:
            Name of the cloud last used in this project.
        """
        cloud_id = self._anyscale_sdk.get_project(project_id).result.last_used_cloud_id
        if not cloud_id:
            msg = (
                "No last active cloud for this project yet. Use "
                "anyscale.cloud('...').connect() to specify a cloud."
            )
            self._log.error(msg)
            raise RuntimeError(msg)

        # TODO(pcm): Replace this with an API call once the AnyscaleSDK supports it.
        p = self._subprocess.Popen(
            ["anyscale", "list", "clouds", "--json"], stdout=subprocess.PIPE
        )
        data = json.loads(p.communicate()[0])
        cloud_name = {elem["id"]: elem["name"] for elem in data}[cloud_id]
        self._log.info(
            (
                f"Using last active cloud '{cloud_name}'. "
                "Call anyscale.cloud('...').connect() to overwrite."
            )
        )
        return cast(str, cloud_name)

    def _get_or_create_updated_session(  # noqa: C901
        self, files_hash: bytes, project_id: str, session_name: Optional[str]
    ) -> str:
        """Get or create a session updated with the given hash.

        Args:
            files_hash (str): The files hash.
            project_id (str): The project to use.
            session_name (Optional[str]): If specified, the given session
                will be created or updated as needed. Otherwise the session
                name will be picked automatically.

        Returns:
            The name of the session to connect to.
        """

        session_hash = None

        if session_name is None:
            self._log.debug("-> Looking for any running session matching hash")
            results = self._list_sessions(project_id=project_id)
            self._log.debug("Session states", [s.state for s in results])
            for session in results:
                if session.state != "Running":
                    continue
                self._log.debug("Trying to acquire lock on", session.name)
                self._tmp_conn = self._acquire_session_lock(
                    session, raise_connection_error=False, connection_retries=0
                )
                if self._tmp_conn is None:
                    continue
                session_hash = self._tmp_conn._internal_kv_get(ANYSCALE_FILES_HASH)
                if session_hash == files_hash:
                    self._log.debug("Acquired lock on session", session.name)
                    session_name = session.name
                    break
                else:
                    self._tmp_conn.disconnect()
                    self._tmp_conn = None

        session_name_conn_failed = None
        if session_name is None:
            self._log.debug("-> Looking for any running session (ignoring hash)")
            for session in results:
                if session.state != "Running":
                    continue
                self._log.debug("Trying to acquire lock on", session.name)
                try:
                    self._tmp_conn = self._acquire_session_lock(
                        session, raise_connection_error=True, connection_retries=0
                    )
                except Exception:
                    self._log.debug(
                        "Error connecting to session, will revisit", session.name
                    )
                    session_name_conn_failed = session.name
                    continue
                if self._tmp_conn:
                    self._log.debug("Acquired lock on session", session.name)
                    session_name = session.name
                    break

        if session_name is None and session_name_conn_failed:
            self._log.debug("-> Fallback to restarting an errored session")
            session_name = session_name_conn_failed

        if session_name is None:
            self._log.debug("-> Fallback to starting a new session")
            used_names = [s.name for s in results if s.state == "Running"]
            for i in range(MAX_SESSIONS):
                name = "session-{}".format(i)
                if name not in used_names:
                    session_name = name
                    self._log.debug("Starting session", session_name)
                    break

        # Should not happen.
        if session_name is None:
            raise RuntimeError("Could not create new session to connect to.")

        if self._cloud_name is None:
            self._cloud_name = self._get_last_used_cloud(project_id)

        self._log.debug("Session hash", session_hash)
        self._log.debug("Local files hash", files_hash)

        if session_hash != files_hash:
            self._log.debug("Syncing latest project files to", session_name)
            # TODO(ekl): race condition here since "up" breaks the lock.
            if self._tmp_conn:
                self._tmp_conn.disconnect()
                self._tmp_conn = None
            # Update session.
            self._up_session(
                project_id, session_name, self._cloud_name, self._project_dir
            )
            # Need to re-acquire the connection after the update.
            self._tmp_conn = self._acquire_session_lock(
                self._get_session_or_die(project_id, session_name),
                raise_connection_error=True,
                connection_retries=10,
            )
            # TODO(ekl) retry this, might be race condition with another client
            if not self._tmp_conn:
                raise RuntimeError("Failed to acquire session we created")
            self._tmp_conn._internal_kv_put(
                ANYSCALE_FILES_HASH, files_hash, overwrite=True
            )
            self._log.debug(
                "Updated files hash",
                files_hash,
                self._tmp_conn._internal_kv_get(ANYSCALE_FILES_HASH),
            )

        return session_name

    def _acquire_session_lock(
        self, session_meta: Any, raise_connection_error: bool, connection_retries: int
    ) -> Optional[Any]:
        """Connect to and acquire a lock on the session.

        The session lock is released by calling disconnect() on the returned
        Ray connection. This function also checks for Python version
        compatibility, it will not acquire the lock on version mismatch.

        Returns:
            Connection to the session, or None if a lock could not be acquired.
        """
        # TODO(ekl) refactor Ray client to avoid this internal API access.
        conn = self._ray.util.client.RayAPIStub()
        session_url, secure, metadata = self._get_connect_params(session_meta)
        if connection_retries > 0:
            self._log.debug("Beginning connection attempts")
        try:
            # Disable retries when acquiring session lock for fast failure.
            info = conn.connect(
                session_url, secure, metadata, connection_retries=connection_retries
            )
        except Exception as e:
            if raise_connection_error:
                self._log.debug(
                    "Connection error after {} retries".format(connection_retries)
                )
                raise
            else:
                self._log.debug("Ignoring connection error", e)
                return None
        if info["num_clients"] > 1:
            conn.disconnect()
            return None
        else:
            return conn

    def _connect_to_session(self, project_id: str, session_name: str) -> None:
        """Connect Ray client to the specified session."""
        session_found = self._get_session_or_die(project_id, session_name)
        session_url, secure, metadata = self._get_connect_params(session_found)
        self._log.debug("Connecting to Ray", session_url, metadata)
        conn_info = self._ray.util.connect(
            session_url, secure=secure, metadata=metadata, connection_retries=3
        )
        self._log.debug("Server info", conn_info)

        def func() -> str:
            return "Connected!"

        f_remote = self._ray.remote(func)
        self._log.debug(self._ray.get(f_remote.remote()))
        self._log.info(
            "Connected to {}, see: {}/o/anyscale-internal/"
            "projects/{}/sessions/{}".format(
                session_name, anyscale.conf.ANYSCALE_HOST, project_id, session_found.id
            )
        )

    def _get_session_or_die(self, project_id: str, session_name: str) -> Session:
        """Query Anyscale for the given session's metadata."""
        session_found = self._get_session(project_id, session_name)
        if not session_found:
            raise RuntimeError("Failed to locate session: {}".format(session_name))
        return session_found

    def _get_session(self, project_id: str, session_name: str) -> Optional[Session]:
        """Query Anyscale for the given session's metadata."""
        results = self._list_sessions(project_id=project_id)
        session_found: Session = None
        for session in results:
            if session.name == session_name:
                session_found = session
                break
        return session_found

    def _get_connect_params(self, session_meta: Session) -> Tuple[str, bool, Any]:
        """Get the params from the session needed to use Ray client."""
        full_url = session_meta.service_proxy_url
        # like "session-fqsx0p3pzfna71xxxxxxx.anyscaleuserdata.com:8081"
        session_url = full_url.split("/")[2].lower() + ":8081"
        # like "8218b528-7363-4d04-8358-57936cdxxxxx"
        auth_token = full_url.split("?token=")[1].split("&")[0]
        metadata = [("cookie", "anyscale-token=" + auth_token), ("port", "10001")]
        return session_url, False, metadata

    def _fingerprint(self, dir_path: str) -> str:
        """Calculate file hash for the given dir."""
        fingerprint_hasher = hashlib.blake2b()
        session_default_yaml = os.path.join(dir_path, "session-default.yaml")
        dir_fingerprint = fingerprint(
            dir_path,
            exclude_dirs=[".git", "__pycache__"],
            exclude_paths=[
                # Ignore the current file, it's not a necessary dependency.
                os.path.abspath(sys.argv[0]),
                # Ignore the session YAMLs since we're updating it.
                session_default_yaml,
                os.path.join(dir_path, ".anyscale.yaml"),
            ],
            mtime_hash=True,
        )
        fingerprint_hasher.update(dir_fingerprint.encode("utf-8"))
        if os.path.exists(session_default_yaml):
            with open(session_default_yaml) as f:
                fingerprint_hasher.update(f.read().encode("utf-8"))
        return fingerprint_hasher.hexdigest()

    def _populate_cluster_config(
        self, cluster_yaml: Dict[str, Any], project_name: str
    ) -> None:
        """Populate cluster config with serverless compute options."""

        base_docker_image_cpu = _get_base_image("cpu")
        base_docker_image_gpu = _get_base_image("gpu")

        # Overwrite base_docker_image if provided by user.
        if self._base_docker_image:
            base_docker_image_cpu = self._base_docker_image
            base_docker_image_gpu = self._base_docker_image
        self._log.debug("Base docker image {}".format(base_docker_image_cpu))

        # Setup serverless compute template.
        cluster_yaml["available_node_types"] = {
            "anyscale.cpu.medium": {
                "node_config": {"InstanceType": "m5.4xlarge"},
                "max_workers": 20,
                # TODO(ekl) why isn't resource autodetect working?
                "resources": {"CPU": 16},
                "docker": {"image": base_docker_image_cpu},
            },
            "anyscale.cpu.large": {
                "node_config": {"InstanceType": "m5.16xlarge"},
                "max_workers": 10,
                "resources": {"CPU": 64},
                "docker": {"image": base_docker_image_cpu},
            },
            "anyscale.gpu.medium": {
                "node_config": {"InstanceType": "g3.4xlarge"},
                "max_workers": 20,
                "resources": {"CPU": 16, "GPU": 1},
                "docker": {"image": base_docker_image_gpu},
            },
            "anyscale.gpu.large": {
                "node_config": {"InstanceType": "g3.16xlarge"},
                "max_workers": 10,
                "resources": {"CPU": 64, "GPU": 4},
                "docker": {"image": base_docker_image_gpu},
            },
        }
        cluster_yaml["max_workers"] = 50
        cluster_yaml["head_node_type"] = "anyscale.cpu.medium"
        cluster_yaml["worker_default_node_type"] = "anyscale.cpu.medium"
        # TODO(ekl) this shouldn't be needed.
        cluster_yaml["docker"]["image"] = base_docker_image_gpu

        # Install Ray runtime if specified.
        if self._ray_release:
            cluster_yaml["setup_commands"] = [
                "pip install -U {}".format(self._get_wheel_url(self._ray_release))
            ]

        # Install requirements:
        if self._requirements:
            cluster_yaml["setup_commands"].append(
                f'echo "{self._requirements}" | pip install -r /dev/stdin'
            )

        # TODO(ekl) we should make the `cd` here standard for all sessions.
        cluster_yaml["head_start_ray_commands"] = [
            "ray stop",
            "ulimit -n 65536; cd ~/"
            + project_name
            + "; AUTOSCALER_UPDATE_INTERVAL_S=5 ray start --head --port=6379 "
            "--object-manager-port=8076 "
            "--ray-client-server-port=10001 "
            "--autoscaling-config=~/ray_bootstrap_config.yaml",
        ]

    def _get_wheel_url(self, ray_release: str) -> str:
        """Return S3 URL for the given release spec or 'latest'."""
        return (
            "https://s3-us-west-2.amazonaws.com/ray-wheels/"
            "{}/ray-2.0.0.dev0-cp37-cp37m-manylinux2014_x86_64.whl".format(
                self._ray_release
            )
        )

    def _get_project_name(self, project_id: str) -> str:
        return self._anyscale_sdk.get_project(project_id).result.name  # type: ignore

    def _list_sessions(self, project_id: str) -> List[Session]:
        sessions = []
        has_more = True
        paging_token = None
        while has_more:
            resp = self._anyscale_sdk.list_sessions(
                project_id, count=50, paging_token=paging_token
            )
            sessions.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = paging_token is not None
        return sessions
