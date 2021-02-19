import json
import time
from logging import config as logging_config
from pathlib import Path

import typer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from certdumper import exc, types
from certdumper.util import clog
from certdumper.conf import config
from certdumper.certs import dump_changed_certs

app = typer.Typer()

logging_config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'certdumper': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
})


@app.command()
def parse(acme_path: str):
    """ Print the parsed ACME configuration.

    Helpful for debugging.
    """
    with open(acme_path) as fp:
        acme = types.AcmeJson(**json.load(fp))

    print(acme.json(indent=2))


@app.command()
def show(
    domain: str,
    acme_path: str = typer.Option(None, '-f', '--acme-file'),
    key_only: bool = typer.Option(False, '--key', is_flag=True),
    cert_only: bool = typer.Option(False, '--cert', is_flag=True),
):
    """ Show certificate and key for a given domain"""
    acme_path = acme_path or config.rel_path(config.acme_path)
    acme = types.AcmeJson.from_file(acme_path)
    cert = acme.find_cert(domain)

    if key_only:
        print(cert.decoded_key)
    if cert_only:
        print(cert.decoded_cert)
    if not (key_only or cert_only):
        print(f"Certificate:\n{cert.decoded_cert}")
        print()
        print(f"Key:\n{cert.decoded_key}")


@app.command()
def watch(acme_path: str = typer.Option(config.acme_path, '-f', '--acme-file')):
    """ Watch acme.json and dump certs to file when they change. """
    path = Path(acme_path)
    if config.work_dir:
        clog(f"-- <32>Using config file <95>{config.config_path}")

    class AcmeFileWatcher(FileSystemEventHandler):
        def on_modified(self, event):
            clog(f"-- <32>File changed: <94>{event.src_path}")
            try:
                dump_changed_certs(Path(event.src_path))
            except exc.InvalidAcmeJson as ex:
                clog(f"-- <31>{str(ex)}")

    while not path.exists():
        clog(f"-- <95>{acme_path} <31>missing")
        time.sleep(5)

    clog(f"-- <32>Watching <95>{acme_path} <32>for changes")
    dump_changed_certs(path)

    event_handler = AcmeFileWatcher()
    observer = Observer()
    observer.schedule(event_handler, acme_path, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
