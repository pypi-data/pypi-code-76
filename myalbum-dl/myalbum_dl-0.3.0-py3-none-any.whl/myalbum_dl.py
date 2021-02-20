import argparse
import concurrent.futures
import glob
import logging
import mimetypes
import os
import platform
import re
import shutil
import sys
import time
import urllib.parse
from threading import Thread, Event

import requests

from .constants import USER_AGENT, DOMAINS, COLORS
if platform.system() == 'Windows':
    from .constants import WIN_SPINNERS as SPINNERS
else:
    from .constants import SPINNERS


class Logger:
    FORMAT = '%(levelname)s: %(message)s'
    FORMAT_DEBUG = '%(asctime) | %(levelname)s: %(message)s'

    def __init__(self, debug):
        self.log = logging.getLogger(__name__)
        if debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        if not self.log.handlers:
            stream_handler = logging.StreamHandler()
            if debug:
                formatter = logging.Formatter(fmt=self.FORMAT_DEBUG)
                stream_handler.setLevel(logging.DEBUG)
            else:
                stream_handler.setLevel(logging.INFO)
                formatter = logging.Formatter(fmt=self.FORMAT)
            stream_handler.setFormatter(fmt=formatter)
            self.log.addHandler(stream_handler)

    def debug(self, message) -> None:
        self.log.debug(message)

    def info(self, message) -> None:
        self.log.info(message)

    def error(self, message) -> None:
        self.log.error(message)


class MyAlbum(Logger):
    def __init__(self, args, cwd=os.getcwd(), title=None,
                 s=None, medias=[], total=0, count=0):
        super().__init__(args.debug)
        self.separate = args.separate
        self.album_json = urllib.parse.urljoin(args.album + '/', 'json')
        self.cwd = cwd
        self.title = title
        self.s = s
        self.medias = medias
        self.total = total
        self.count = count

    def scrape_album(self) -> None:
        self.create_session()
        r = self.get_response()
        self.parse_response(r.json())
        self.log.info(f"{self.title}")
        self.total = len(self.medias)

    def create_session(self) -> None:
        s = requests.Session()
        headers = {
            'user-agent': USER_AGENT,
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'x-requested-with': 'XMLHttpRequest',
            'referer': self.album_json.rsplit('/json', 1)[0]
        }
        s.headers.update(headers)
        self.s = s

    def get_response(self) -> requests.models.Response or None:
        with self.s.get(self.album_json) as r:
            if r.ok:
                return r
            else:
                self.log.error(
                    f"Unable to get album——STATUS CODE: {r.status_code}")
                return

    def parse_response(self, response) -> None:
        self.title = self.clean_text(response['album']['title'])
        itemdata = response['itemdata']
        ids = list(itemdata)
        for id_ in ids:
            media = itemdata[id_]
            if media['type'] == 10:
                media_url = media['sizes'][-1][-2]
                filename = media['photo']['fileName'].rsplit('.', 1)[
                    0] + '.mp4'
                self.medias.append((media_url, filename))
            elif media['type'] == 1:
                media_url = media['sizes'][-1][-2]
                filename = media['fileName']
                self.medias.append((media_url, filename))
            else:
                continue

    def prepare_download(self) -> None:
        if self.medias:
            self.s.headers.update(
                {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
            os.makedirs(os.path.join(self.cwd, self.title), exist_ok=True)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self.download, media): media for media in self.medias}
                for future in concurrent.futures.as_completed(futures):
                    future.result
            if self.separate:
                self.separate_media()
        else:
            self.log.info(f"Found 0 items in album——quitting program")
            return

    def download(self, media) -> None:
        count = 0
        while True:
            url = DOMAINS[count] + media[0]
            filename = media[1]
            with self.s.get(url) as r:
                if not r.ok:
                    count += 1
                else:
                    with open(os.path.join(self.cwd, self.title, filename), 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            f.write(chunk)
                    self.count += 1
                    break
            if count > 2:
                self.log.error(
                    f"Unable to download media ({filename})——STATUS CODE: {r.status_code}")

    def separate_media(self) -> None:
        dir_ = os.path.join(self.cwd, self.title)
        files = glob.glob(dir_ + '\\*.*')
        if files:
            image_pattern = re.compile(r'image/\w+')
            video_pattern = re.compile(r'video/\w+')
            image_files, video_files = [], []
            for file in files:
                try:
                    if re.search(image_pattern, mimetypes.guess_type(file)[0]):
                        image_files.append(file)
                    elif re.search(video_pattern, mimetypes.guess_type(file)[0]):
                        video_files.append(file)
                    else:
                        pass
                except TypeError:
                    pass
            if image_files:
                image_dir = os.path.join(dir_, 'Images')
                os.makedirs(image_dir, exist_ok=True)
                for file in image_files:
                    shutil.move(os.path.join(dir_, file), image_dir)
            if video_files:
                video_dir = os.path.join(dir_, 'Videos')
                os.makedirs(video_dir, exist_ok=True)
                for file in video_files:
                    shutil.move(os.path.join(dir_, file), video_dir)
        return

    def spinner(self, event) -> None:
        while True:
            for color in COLORS:
                for spinner in SPINNERS:
                    if event.is_set():
                        return
                    print(f' {color[0]}{spinner}{color[1]} [{self.count}/{self.total}]',
                          end='\r', flush=True)
                    time.sleep(0.1)

    @staticmethod
    def clean_text(text) -> str:
        pattern = re.compile(r'[\\/:*?"<>|]')
        cleaned_text = re.sub(pattern, '_', text)
        return cleaned_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'album', type=str, help="URL of the album to scrape")
    parser.add_argument(
        '--debug', help="option to enable debugging", action='store_true')
    parser.add_argument(
        '-s', '--separate', help="separate media types into their own directories", action='store_true')
    if platform.system() == 'Windows':
        os.system('color')
    args = parser.parse_args()
    myalbum = MyAlbum(args)
    myalbum.scrape_album()
    e1 = Event()
    t1 = Thread(target=myalbum.spinner, args=(e1,))
    t1.start()
    myalbum.prepare_download()
    e1.set()


if __name__ == '__main__':
    main()
