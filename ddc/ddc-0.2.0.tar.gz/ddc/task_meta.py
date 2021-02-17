import time
import logging
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
import os
import threading
from ddc.utils import read_ddc_file, write_ddc_file, get_path_ddc_file, stream_exec_cmd

META_DOCKER_COMPOSE_FILENAME = "meta-docker-compose.yaml"

ACTUAL_DOCKER_COMPOSE_FILE = """
version: '3'
services:
  redis:
    image: redis:alpine
  meta:
    image: apisgarpun/metaplatform:latest
    depends_on:
      - redis
    ports:
      - "9999:8080"
    volumes:
      - ~/.rwmeta:/root/.rwmeta:delegated
      - ./meta_conf:/root/meta_conf:delegated
      - ./:/root/workspace/production:delegated
    environment:
      JAVA_OPTS: -Duser.timezone=Europe/Moscow -Xms1000m -Xmx2500m -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9010 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=localhost
      META_CONFIG: /root/meta_conf/meta-loc-dev.yaml
      RELEASE_VERSION2: dev
      RELEASE_VERSION: local_dev
      META_APP_CONTENT_CONFIG_DIR: /root/meta_conf
      META_APP_CONTENT_WORKSPACE_DIR: /root/workspace
"""  # noqa


class GitAddEventHandler(RegexMatchingEventHandler):
    IMAGES_REGEX = [r".*\.html"]

    def __init__(self):
        super().__init__(self.IMAGES_REGEX)

    def on_moved(self, event):
        super(GitAddEventHandler, self).on_moved(event)

        self.__git_add_file(event.src_path)

    def on_created(self, event):
        super(GitAddEventHandler, self).on_created(event)
        self.__git_add_file(event.src_path)

    def __git_add_file(self, file_path: str):
        if file_path.endswith(".html"):
            os.system("git add " + file_path)
            logging.info("git add = %s" % str(file_path))


def start_add_file_watchdog(path):
    logging.info("Start new html files watchdog")

    event_handler = GitAddEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class AddFilesThread(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        start_add_file_watchdog(self.path)


def start_meta(cwd):
    AddFilesThread(cwd).start()

    current_compose_content = read_ddc_file(META_DOCKER_COMPOSE_FILENAME)
    if not current_compose_content:
        current_compose_content = ""
    if current_compose_content != ACTUAL_DOCKER_COMPOSE_FILE:
        write_ddc_file(META_DOCKER_COMPOSE_FILENAME, ACTUAL_DOCKER_COMPOSE_FILE)

    compose_file = get_path_ddc_file(META_DOCKER_COMPOSE_FILENAME)

    compose_base_cmd = "docker-compose -f {compose_file} -p ddc_meta --project-directory={cwd}".format(
        compose_file=compose_file, cwd=cwd
    )

    stream_exec_cmd(compose_base_cmd + " down")
    try:
        stream_exec_cmd(compose_base_cmd + " pull")
        stream_exec_cmd(compose_base_cmd + " up")
    finally:
        stream_exec_cmd(compose_base_cmd + " down")
