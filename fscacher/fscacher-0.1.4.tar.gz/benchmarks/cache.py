from hashlib import sha256
import os
from pathlib import Path
import random
import shutil
from time import sleep, time
from uuid import uuid4
from morecontext import envset
from fscacher import PersistentCache


class TimeFile:

    FILE_SIZE = 1024
    param_names = ["control"]
    params = (["", "ignore"])

    def setup_cache(self):
        with open("foo.dat", "wb") as fp:
            fp.write(bytes(random.choices(range(256), k=self.FILE_SIZE)))

    def setup(self, control):
        with envset("FSCACHER_CACHE", control):
            self.cache = PersistentCache(name=str(uuid4()))

        @self.cache.memoize_path
        def hashfile(path):
            # "emulate" slow invocation so significant raise in benchmark
            # consumed time would mean that we invoked it instead
            # of using cached value
            sleep(0.01)
            with open(path, "rb") as fp:
                return sha256(fp.read()).hexdigest()
        self._hashfile = hashfile

    def time_file(self, control):
        for _ in range(100):
            self._hashfile("foo.dat")

    def teardown(self, control):
        self.cache.clear()


class TimeDirectoryFlat:

    LAYOUT = (100,)

    param_names = ["control", "tmpdir"]
    params = (
        ["", "ignore"],
        os.environ.get("FSCACHER_BENCH_TMPDIRS", ".").split(":"),
    )

    def setup(self, control, tmpdir):
        cache_id = str(uuid4())
        with envset("FSCACHER_CACHE", control):
            self.cache = PersistentCache(name=cache_id)
        self.dir = Path(tmpdir, cache_id)
        self.dir.mkdir()
        create_tree(self.dir, self.LAYOUT)

        @self.cache.memoize_path
        def dirsize(path):
            total_size = 0
            with os.scandir(path) as entries:
                for e in entries:
                    if e.is_dir():
                        total_size += dirsize(e.path)
                    else:
                        total_size += e.stat().st_size
            return total_size
        self._dirsize = dirsize

    def time_directory(self, control, tmpdir):
        for _ in range(100):
            self._dirsize(str(self.dir))

    def teardown(self, *args, **kwargs):
        self.cache.clear()
        shutil.rmtree(self.dir)


class TimeDirectoryDeep(TimeDirectoryFlat):
    LAYOUT = (3, 3, 3, 3)


def create_tree(root, layout):
    base_time = time()
    dirs = [Path(root)]
    for i, width in enumerate(layout):
        if i < len(layout) - 1:
            dirs2 = []
            for d in dirs:
                for x in range(width):
                    d2 = d / f"d{x}"
                    d2.mkdir()
                    dirs2.append(d2)
            dirs = dirs2
        else:
            for j, d in enumerate(dirs):
                for x in range(width):
                    f = d / f"f{x}.dat"
                    f.write_bytes(b"\0" * random.randint(1, 1024))
                    t = base_time - x - j * width
                    os.utime(f, (t, t))
