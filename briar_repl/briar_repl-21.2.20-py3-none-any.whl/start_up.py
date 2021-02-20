import os
import errno
import psutil
from pathlib import Path
import colorful as col
from dataclasses import dataclass
from .__init__ import __version__


@dataclass
class App:
    pid     : int
    version : str  = __version__
    name    : str  = "briar_repl"
    bh_pid  : int  = 0


@dataclass
class Urls:
    base             : str
    contacts         : str
    contacts_pending : str
    link             : str
    msgs             : str
    blogs            : str
    ws               : str


def get_auth_token(briar_dir: Path):
    AUTH_FILE = briar_dir / "auth_token"
    if not AUTH_FILE.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), AUTH_FILE)
    with open(AUTH_FILE) as txt:
        token = txt.read().strip()
        return {'Authorization': f'Bearer {token}'}, token


def briar_headless_process_running():
    for p in psutil.process_iter(['name', 'cmdline']):
        if not p.info["name"] == "java":
            continue
        if "briar-headless" in str(p.cmdline()):
            print(col.bold_chartreuse("briar-headless is already running!"))
            return True
    print(col.coral("briar-headless not running!"))
    return False


def get_headless_jar_path(headless_dir):
    if not headless_dir.exists():
        FLATPAK_HEADLESS_JAR_PATH = Path("/app/share/java/briar-headless.jar")
        if FLATPAK_HEADLESS_JAR_PATH.exists():
             return FLATPAK_HEADLESS_JAR_PATH
        print(col.coral(f"could not find 'briar-headless.jar' in {headless_dir}"))
        quit(1)
    for node in headless_dir.iterdir():
        if node.suffix != ".jar":
            continue
        if "briar-headless" in node.name:
            headless_jar_path = node.absolute()
            print(col.bold_chartreuse(f"found {headless_jar_path}!"))
            return headless_jar_path
    print(col.coral(f"could not find 'briar-headless.jar' in {headless_dir}"))
    quit(1)


def on_terminate(proc):
    print(f"process {proc} terminated with exit code {proc.returncode}")
    quit(3)


BRIAR_HOME = Path(Path().home().absolute()) / ".briar"

headless_is_running = briar_headless_process_running()

if not headless_is_running:

    HEADLESS_DIR = BRIAR_HOME / "headless"
    HEADLESS_JAR_PATH = get_headless_jar_path(HEADLESS_DIR)

    cmd_str = f"java -jar {HEADLESS_JAR_PATH}"
    print(f"running briar-headless from: {HEADLESS_JAR_PATH}")
    headless_proc = psutil.Popen(cmd_str.split(), stdout=None)
    gone, alive = psutil.wait_procs(
        [headless_proc],
        timeout=25,
        callback=on_terminate,
    )
    print(gone, alive)
    print(f"briar-headless pid: {headless_proc.pid}")
    print("waiting for briar_headless to start up..")

APP = App(pid=os.getpid())
AUTH, TOKEN = get_auth_token(BRIAR_HOME)
HOST = "127.0.0.1"
PORT = 7000
API_VERSION = "v1"
URL_BASE = f'http://{HOST}:{PORT}/{API_VERSION}/'
print(f"\nwelcome to {col.bold_chartreuse(APP.name)}!")
print("to list all functionality enter 'help'.\n")

URLS = Urls(
    base            =URL_BASE,
    contacts        =f"{URL_BASE}contacts",
    contacts_pending=f"{URL_BASE}contacts/add/pending",
    link            =f"{URL_BASE}contacts/add/link",
    msgs            =f"{URL_BASE}messages/",
    blogs           =f"{URL_BASE}blogs/posts",
    ws              =f'ws://{HOST}:{PORT}/{API_VERSION}/ws',
)
